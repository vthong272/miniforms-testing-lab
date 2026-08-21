# Bộ nộp bài MiniForms SWT301

## 1. Báo cáo

File khuyến nghị: `MiniForms_Overleaf_Report_VI_FIXED.zip`

Trên Overleaf chọn **New Project > Upload Project**, tải nguyên file ZIP này lên,
chọn compiler **pdfLaTeX**, main document `main.tex`, sau đó chọn **Recompile**.
Không dán riêng fragment bắt đầu bằng đoạn `EP, BVA và DTT...` vì fragment đó
thiếu preamble và `\\begin{document}`. Nếu chỉ muốn thay file trong project cũ,
dùng `main_fixed.tex` và đổi tên thành `main.tex`.

Trang đầu dùng block tác giả của `tham-khao-en.tex`: ba tác giả, một dòng
`FPT University, Ho Chi Minh City, Vietnam` và ba email. Không hiển thị lớp hoặc
giảng viên trong block tác giả.

## 2. Source code và bằng chứng thực nghiệm

File: `MiniForms_Source_Code_Experiment.zip`

Gói source được nộp riêng, gồm Golden Version, 18 mutant, 110 test case, Selenium runner, scripts, mutation matrix, metrics, 57 JUnit report và 57 log.

## 3. Kiểm tra trước khi nộp

Đọc `submission/SUBMISSION_CHECKLIST.md` trong repository. Không sửa dữ liệu Frozen v1.0 hoặc số liệu báo cáo nếu không chạy lại toàn bộ thí nghiệm.

## Kết quả đã xác minh

- Python unit test: 10/10 pass.
- JavaScript unit test: 10/10 pass.
- Mutant verification: 18/18 hợp lệ.
- Golden Selenium: 110/110 pass.
- Report static validation: pass, 7 citations, 17 labels và 3 biểu đồ PDF vector.
