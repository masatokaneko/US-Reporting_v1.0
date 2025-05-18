/**
 * APIエラークラス
 * @extends Error
 */
class ApiError extends Error {
  /**
   * @param {number} statusCode - HTTPステータスコード
   * @param {string} code - エラーコード
   * @param {string} message - エラーメッセージ
   */
  constructor(statusCode, code, message) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.name = 'ApiError';
  }
}

/**
 * エラーハンドラーミドルウェア
 * @param {Error} err - エラーオブジェクト
 * @param {Object} req - リクエストオブジェクト
 * @param {Object} res - レスポンスオブジェクト
 * @param {Function} next - 次のミドルウェア
 */
const errorHandler = (err, req, res, next) => {
  console.error(err);
  
  if (err instanceof ApiError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message
      },
      meta: {
        timestamp: new Date().toISOString(),
        request_id: req.requestId
      }
    });
  }
  
  // データベースエラー
  if (err.code === '23505') { // 一意制約違反
    return res.status(409).json({
      success: false,
      error: {
        code: 'DUPLICATE_ENTRY',
        message: '既に存在するデータです'
      },
      meta: {
        timestamp: new Date().toISOString(),
        request_id: req.requestId
      }
    });
  }
  
  // その他のエラー
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'サーバーエラーが発生しました'
    },
    meta: {
      timestamp: new Date().toISOString(),
      request_id: req.requestId
    }
  });
};

module.exports = {
  ApiError,
  errorHandler
}; 