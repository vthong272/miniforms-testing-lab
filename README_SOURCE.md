# MiniForms Research Artifact

Gói này chứa mã nguồn và bằng chứng tái lập cho nghiên cứu so sánh Equivalence Partitioning (EP), Boundary Value Analysis (BVA) và Decision Table Testing (DTT).

## Thành phần

- `app/`: Golden web application và 18 mutant M01--M18.
- `requirements/`: đặc tả business rules của ba form.
- `test-design/`: mốc Frozen v1.0.
- `tests/frozen_cases.py`: nguồn dữ liệu duy nhất cho 110 ca kiểm thử.
- `tests/selenium/`: Selenium runner dùng chung.
- `scripts/`: sinh mutant, xác minh mutant, chạy thí nghiệm và tính metrics.
- `experiment-results/frozen-v1.0-run-20260814/`: mutation matrix, metrics, 57 JUnit report và log.
- `mutant-manifest.json`, `mutant-manifest.csv`: danh mục và witness của 18 mutant.

## Yêu cầu môi trường

- Python 3.11 trở lên.
- Google Chrome.
- Node.js 18 trở lên để chạy unit test JavaScript.

## Cài đặt

Trên PowerShell, tại thư mục source:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Selenium Manager sẽ tự tìm ChromeDriver tương thích khi có kết nối mạng.

## Chạy ứng dụng

```powershell
python -m http.server 8000 --directory app
```

Mở `http://127.0.0.1:8000/` để xem golden. Để chạy trực tiếp một mutant, thêm query parameter, ví dụ:

- `http://127.0.0.1:8000/?variant=M01#registration`
- `http://127.0.0.1:8000/?variant=M09#shipping`
- `http://127.0.0.1:8000/?variant=M15#loan`

## Kiểm tra Golden Version

```powershell
.venv\Scripts\python.exe -m pytest tests/selenium/test_frozen_golden.py -q
```

Kết quả bắt buộc:

- EP: 30/30.
- BVA: 51/51.
- DTT: 29/29.
- Tổng: 110/110.

Chạy riêng một kỹ thuật bằng `-m ep`, `-m bva` hoặc `-m dtt`.

## Tái lập thí nghiệm mutation

```powershell
.venv\Scripts\python.exe -m scripts.generate_mutants
.venv\Scripts\python.exe -m scripts.verify_mutants
.venv\Scripts\python.exe -m scripts.run_experiment
```

Runner kiểm tra hash Frozen v1.0, yêu cầu golden pass trước, chạy 54 lượt mutant và chỉ tính killed khi có assertion failure hợp lệ. Kết quả mới được tạo trong `experiment-results/`.

## Kết quả chuẩn ngày 14/08/2026

| Suite | Test cases | Killed | DDR | Efficiency |
|---|---:|---:|---:|---:|
| EP | 30 | 10/18 | 55.56% | 0.3333 |
| BVA | 51 | 9/18 | 50.00% | 0.1765 |
| DTT | 29 | 7/18 | 38.89% | 0.2414 |

Combined effectiveness: 18/18 mutant, DDR 100%.

## Quy tắc nghiên cứu

Không sửa test ID, input hoặc expected result của Frozen v1.0 sau khi xem mutant. Nếu phát hiện lỗi trong thiết kế test, phải tạo phiên bản Frozen mới, ghi lý do, review chéo và chạy lại toàn bộ golden/mutant.
