# Hướng dẫn dùng trên Overleaf

1. Tạo project mới trên Overleaf bằng **New Project > Upload Project**.
2. Upload toàn bộ file `MiniForms_Overleaf_Report_VI.zip`.
3. Mở **Menu > Compiler** và chọn **pdfLaTeX**.
4. Đặt **Main document** là `main.tex`.
5. Chọn **Recompile**. Overleaf sẽ tự chạy BibTeX để tạo danh mục tài liệu tham khảo.

## Nếu Overleaf báo `Missing \\begin{document}`

Không dán riêng đoạn bắt đầu bằng nội dung `EP, BVA và DTT...` vào sau
`\\documentclass`. Đó chỉ là một đoạn giữa bài. Hãy upload nguyên ZIP hoặc thay
toàn bộ file bằng `main.tex` trong gói này; file hoàn chỉnh có preamble,
`\\begin{document}`, tiêu đề, abstract và `\\end{document}`.

## Nội dung gói

- `main.tex`: báo cáo tiếng Việt theo định dạng Springer LLNCS.
- `references.bib`: tài liệu tham khảo.
- `llncs.cls`, `splncs04.bst`: class và bibliography style từ file mẫu.
- `figures/`: ba biểu đồ được sinh từ kết quả thực nghiệm thật.

## Dữ liệu được cố định trong báo cáo

- EP: 30 ca, killed 10/18, DDR 55,56%, efficiency 0,3333.
- BVA: 51 ca, killed 9/18, DDR 50,00%, efficiency 0,1765.
- DTT: 29 ca, killed 7/18, DDR 38,89%, efficiency 0,2414.
- Combined: killed 18/18, DDR 100%.

Không sửa các con số trên nếu không chạy lại toàn bộ thí nghiệm và cập nhật mutation matrix.
