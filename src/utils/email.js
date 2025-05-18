const nodemailer = require('nodemailer');
const config = require('../config');

// メール送信用トランスポート設定
const transporter = nodemailer.createTransport({
  host: config.email.host,
  port: config.email.port,
  secure: config.email.secure,
  auth: {
    user: config.email.user,
    pass: config.email.password
  }
});

/**
 * 見積書メール送信
 * @param {Object} options - メール送信オプション
 * @returns {Promise<Object>} - 送信結果
 */
const sendQuotationEmail = async (options) => {
  const { to, cc, subject, body, attachments } = options;
  
  const mailOptions = {
    from: `"${config.company.name}" <${config.email.from}>`,
    to,
    cc: cc || [],
    subject,
    html: `
      <p>${body}</p>
      <p>--<br>
      ${config.company.name}<br>
      ${config.company.address}<br>
      Tel: ${config.company.phone}<br>
      Email: ${config.company.email}<br>
      Website: ${config.company.website}</p>
    `,
    attachments
  };
  
  return transporter.sendMail(mailOptions);
};

/**
 * 請求書メール送信
 * @param {Object} options - メール送信オプション
 * @returns {Promise<Object>} - 送信結果
 */
const sendInvoiceEmail = async (options) => {
  const { to, cc, subject, body, attachments } = options;
  
  const mailOptions = {
    from: `"${config.company.name}" <${config.email.from}>`,
    to,
    cc: cc || [],
    subject,
    html: `
      <p>${body}</p>
      <p>--<br>
      ${config.company.name}<br>
      ${config.company.address}<br>
      Tel: ${config.company.phone}<br>
      Email: ${config.company.email}<br>
      Website: ${config.company.website}</p>
    `,
    attachments
  };
  
  return transporter.sendMail(mailOptions);
};

module.exports = {
  sendQuotationEmail,
  sendInvoiceEmail
}; 