const jwt = require('jsonwebtoken');
const { ApiError } = require('../../utils/errors');
const config = require('../../config');

/**
 * JWT認証ミドルウェア
 * @param {Object} req - リクエストオブジェクト
 * @param {Object} res - レスポンスオブジェクト
 * @param {Function} next - 次のミドルウェア
 */
const authenticateJWT = (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      throw new ApiError(401, 'UNAUTHORIZED', '認証が必要です');
    }
    
    const token = authHeader.split(' ')[1];
    
    if (!token) {
      throw new ApiError(401, 'UNAUTHORIZED', 'トークンが無効です');
    }
    
    jwt.verify(token, config.jwtSecret, (err, decoded) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          throw new ApiError(401, 'TOKEN_EXPIRED', 'トークンの有効期限が切れています');
        }
        throw new ApiError(401, 'INVALID_TOKEN', 'トークンが無効です');
      }
      
      req.user = decoded;
      next();
    });
  } catch (error) {
    next(error);
  }
};

/**
 * 権限チェックミドルウェア
 * @param {string[]} requiredPermissions - 必要な権限の配列
 * @returns {Function} - ミドルウェア関数
 */
const checkPermissions = (requiredPermissions) => {
  return (req, res, next) => {
    try {
      if (!req.user) {
        throw new ApiError(401, 'UNAUTHORIZED', '認証が必要です');
      }
      
      const hasPermission = requiredPermissions.every(permission =>
        req.user.permissions.includes(permission)
      );
      
      if (!hasPermission) {
        throw new ApiError(403, 'FORBIDDEN', '権限がありません');
      }
      
      next();
    } catch (error) {
      next(error);
    }
  };
};

module.exports = {
  authenticateJWT,
  checkPermissions
}; 