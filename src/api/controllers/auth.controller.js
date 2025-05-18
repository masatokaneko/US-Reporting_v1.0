const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { pool } = require('../../db');
const { ApiError } = require('../../utils/errors');
const config = require('../../config');
const { v4: uuidv4 } = require('uuid');

/**
 * ユーザーログイン
 * @param {Object} req - リクエストオブジェクト
 * @param {Object} res - レスポンスオブジェクト
 * @param {Function} next - 次のミドルウェア
 * @returns {Object} - レスポンス
 */
const login = async (req, res, next) => {
  try {
    const { email, password } = req.body;
    
    // バリデーション
    if (!email || !password) {
      throw new ApiError(400, 'INVALID_INPUT', 'メールアドレスとパスワードは必須です');
    }
    
    // ユーザー検索
    const query = `
      SELECT 
        u.*,
        CASE WHEN u.admin_permission THEN true ELSE false END as is_admin,
        array_agg(r.role_name) as roles
      FROM 
        users u
        LEFT JOIN user_roles ur ON u.user_id = ur.user_id
        LEFT JOIN roles r ON ur.role_id = r.role_id
      WHERE 
        u.email = $1 AND u.status = 'active'
      GROUP BY 
        u.user_id
    `;
    
    const result = await pool.query(query, [email]);
    
    if (result.rows.length === 0) {
      throw new ApiError(401, 'INVALID_CREDENTIALS', 'メールアドレスまたはパスワードが正しくありません');
    }
    
    const user = result.rows[0];
    
    // パスワード検証
    const passwordMatch = await bcrypt.compare(password, user.password_hash);
    
    if (!passwordMatch) {
      throw new ApiError(401, 'INVALID_CREDENTIALS', 'メールアドレスまたはパスワードが正しくありません');
    }
    
    // 権限情報の整理
    const permissions = [];
    
    if (user.create_quote_permission) permissions.push('create_quote');
    if (user.approve_quote_permission) permissions.push('approve_quote');
    if (user.manage_order_permission) permissions.push('manage_order');
    if (user.create_invoice_permission) permissions.push('create_invoice');
    if (user.approve_invoice_permission) permissions.push('approve_invoice');
    if (user.manage_revenue_permission) permissions.push('manage_revenue');
    if (user.admin_permission) permissions.push('admin');
    
    // JWTトークンの生成
    const token = jwt.sign(
      {
        userId: user.user_id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        isAdmin: user.is_admin,
        permissions
      },
      config.jwtSecret,
      { expiresIn: '1h' }
    );
    
    // リフレッシュトークンの生成
    const refreshToken = jwt.sign(
      { userId: user.user_id },
      config.refreshTokenSecret,
      { expiresIn: '30d' }
    );
    
    // 最終ログイン日時の更新
    const updateQuery = `
      UPDATE users
      SET last_login = NOW()
      WHERE user_id = $1
    `;
    
    await pool.query(updateQuery, [user.user_id]);
    
    // 活動ログ記録
    const logInsertQuery = `
      INSERT INTO activity_logs (
        log_id, user_id, activity_type, entity_type, entity_id,
        description, ip_address, user_agent, created_at
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, NOW()
      )
    `;
    
    await pool.query(logInsertQuery, [
      uuidv4(), user.user_id, 'LOGIN', 'user', user.user_id,
      'ユーザーがログインしました',
      req.ip,
      req.get('User-Agent')
    ]);
    
    return res.json({
      success: true,
      data: {
        token,
        refresh_token: refreshToken,
        expires_in: 3600,
        user: {
          user_id: user.user_id,
          email: user.email,
          first_name: user.first_name,
          last_name: user.last_name,
          role: user.roles.filter(r => r !== null),
          permissions
        }
      },
      meta: {
        timestamp: new Date().toISOString(),
        request_id: req.requestId
      }
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  login
}; 