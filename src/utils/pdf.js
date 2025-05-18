const PDFDocument = require('pdfkit');
const fs = require('fs');

/**
 * PDF生成
 * @param {string} type - ドキュメントタイプ（'quotation'または'invoice'）
 * @param {Object} data - PDF生成に必要なデータ
 * @returns {Promise<Buffer>} - 生成されたPDFのバッファ
 */
const createPdf = (type, data) => {
  return new Promise((resolve, reject) => {
    try {
      const doc = new PDFDocument({ margin: 50 });
      const chunks = [];
      
      doc.on('data', chunk => chunks.push(chunk));
      doc.on('end', () => resolve(Buffer.concat(chunks)));
      
      // 共通ヘッダー
      doc.fontSize(20).text(`${type === 'quotation' ? '見積書' : '請求書'}`, { align: 'center' });
      doc.moveDown();
      
      // 文書番号
      const documentNumber = type === 'quotation' ? data.quotation.quotation_number : data.invoice.invoice_number;
      doc.fontSize(12).text(`${type === 'quotation' ? '見積書番号' : '請求書番号'}: ${documentNumber}`);
      
      // 日付
      const documentDate = type === 'quotation' ? data.quotation.quotation_date : data.invoice.invoice_date;
      doc.text(`${type === 'quotation' ? '見積日' : '請求日'}: ${formatDate(documentDate)}`);
      
      if (type === 'quotation') {
        doc.text(`有効期限: ${formatDate(data.quotation.expiration_date)}`);
      } else {
        doc.text(`支払期限: ${formatDate(data.invoice.due_date)}`);
      }
      
      doc.moveDown();
      
      // 顧客情報
      const customer = type === 'quotation' ? data.quotation : data.invoice;
      doc.fontSize(14).text('宛先:');
      doc.fontSize(12).text(customer.company_name);
      doc.text(customer.address_line1);
      if (customer.address_line2) doc.text(customer.address_line2);
      doc.text(`${customer.city}, ${customer.state} ${customer.zip_code}`);
      doc.text(customer.country);
      
      doc.moveDown();
      
      // 自社情報
      doc.fontSize(14).text('発行元:');
      doc.fontSize(12).text(data.company.name);
      doc.text(data.company.address);
      doc.text(`TEL: ${data.company.phone}`);
      doc.text(`Email: ${data.company.email}`);
      doc.text(`Web: ${data.company.website}`);
      
      doc.moveDown(2);
      
      // 明細表のヘッダー
      const tableTop = doc.y;
      const tableHeaders = ['項目', '数量', '単価', '金額(税抜)', '税率', '税額', '金額(税込)'];
      const columnWidths = [200, 40, 70, 70, 40, 60, 70];
      
      let currentX = 50;
      doc.fontSize(10).font('Helvetica-Bold');
      
      tableHeaders.forEach((header, i) => {
        const width = columnWidths[i];
        doc.text(header, currentX, tableTop, { width, align: i === 0 ? 'left' : 'right' });
        currentX += width;
      });
      
      // 明細行
      doc.font('Helvetica');
      let currentY = tableTop + 20;
      
      data.items.forEach(item => {
        currentX = 50;
        
        // 商品名/説明
        const productText = `${item.product_name}\n${item.description || ''}`;
        doc.text(productText, currentX, currentY, { width: columnWidths[0] });
        currentX += columnWidths[0];
        
        // 数量
        doc.text(item.quantity.toString(), currentX, currentY, { width: columnWidths[1], align: 'right' });
        currentX += columnWidths[1];
        
        // 単価
        doc.text(formatCurrency(item.unit_price), currentX, currentY, { width: columnWidths[2], align: 'right' });
        currentX += columnWidths[2];
        
        // 小計
        doc.text(formatCurrency(item.subtotal), currentX, currentY, { width: columnWidths[3], align: 'right' });
        currentX += columnWidths[3];
        
        // 税率
        doc.text(`${item.tax_rate}%`, currentX, currentY, { width: columnWidths[4], align: 'right' });
        currentX += columnWidths[4];
        
        // 税額
        doc.text(formatCurrency(item.tax_amount), currentX, currentY, { width: columnWidths[5], align: 'right' });
        currentX += columnWidths[5];
        
        // 合計
        doc.text(formatCurrency(item.total_amount), currentX, currentY, { width: columnWidths[6], align: 'right' });
        
        // 次の行へ
        const textHeight = doc.heightOfString(productText, { width: columnWidths[0] });
        currentY += Math.max(textHeight, 20) + 10;
      });
      
      // 罫線
      doc.moveTo(50, tableTop + 15).lineTo(550, tableTop + 15).stroke();
      doc.moveTo(50, currentY - 5).lineTo(550, currentY - 5).stroke();
      
      // 合計欄
      currentY += 10;
      doc.font('Helvetica-Bold');
      
      const totals = type === 'quotation' ? data.quotation : data.invoice;
      
      doc.text('小計:', 380, currentY, { width: 100, align: 'right' });
      doc.text(formatCurrency(totals.subtotal), 480, currentY, { width: 70, align: 'right' });
      currentY += 20;
      
      doc.text('消費税:', 380, currentY, { width: 100, align: 'right' });
      doc.text(formatCurrency(totals.tax_amount), 480, currentY, { width: 70, align: 'right' });
      currentY += 20;
      
      doc.text('合計:', 380, currentY, { width: 100, align: 'right' });
      doc.text(formatCurrency(totals.total_amount), 480, currentY, { width: 70, align: 'right' });
      
      // 請求書の場合は支払い情報を追加
      if (type === 'invoice') {
        currentY += 40;
        doc.fontSize(12).text('支払い情報:', 50, currentY);
        currentY += 20;
        
        doc.fontSize(10).font('Helvetica');
        doc.text(`銀行名: ${data.invoice.bank_name}`, 50, currentY);
        currentY += 15;
        doc.text(`支店名: ${data.invoice.bank_branch}`, 50, currentY);
        currentY += 15;
        doc.text(`口座番号: ${data.invoice.account_number}`, 50, currentY);
        currentY += 15;
        doc.text(`口座名義: ${data.invoice.account_name}`, 50, currentY);
        currentY += 15;
        doc.text(`SWIFTコード: ${data.invoice.swift_code}`, 50, currentY);
        currentY += 15;
        doc.text(`ABA/ルーティング: ${data.invoice.aba_routing}`, 50, currentY);
      }
      
      // 備考
      if ((type === 'quotation' && data.quotation.notes) || 
          (type === 'invoice' && data.invoice.notes)) {
        currentY += 40;
        doc.fontSize(12).text('備考:', 50, currentY);
        currentY += 20;
        
        const notes = type === 'quotation' ? data.quotation.notes : data.invoice.notes;
        doc.fontSize(10).font('Helvetica').text(notes, 50, currentY, { width: 500 });
      }
      
      // PDF生成完了
      doc.end();
    } catch (error) {
      reject(error);
    }
  });
};

// 日付フォーマット
function formatDate(date) {
  if (!date) return '';
  
  if (typeof date === 'string') {
    date = new Date(date);
  }
  
  return date.toISOString().split('T')[0];
}

// 金額フォーマット
function formatCurrency(amount) {
  return parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

module.exports = {
  createPdf
}; 