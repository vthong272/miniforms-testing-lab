# So sánh EP, BVA và Decision Table Testing trong Web Form Business Logic

## Research question

**How do Equivalence Partitioning (EP), Boundary Value Analysis (BVA), and
Decision Table Testing (DTT) compare in terms of Defect Detection Rates and Test
Suite Efficiency in Web Form Business Logic?**

Nghiên cứu kiểm tra bốn câu hỏi cụ thể: EP có mạnh nhất với partition defects
không; BVA có mạnh nhất với boundary defects không; DTT có mạnh nhất với
decision-rule defects không; và việc kết hợp cả ba kỹ thuật có phát hiện được
nhiều lỗi hơn từng kỹ thuật riêng lẻ không.

## Methodology

Nghiên cứu được thiết kế dưới dạng **controlled benchmark pilot study**. Đối
tượng thử nghiệm là MiniForms, một ứng dụng HTML/CSS/JavaScript thuần gồm ba
web form: Registration, Shipping & Discount và Loan Eligibility. Biến độc lập
là kỹ thuật thiết kế test (EP, BVA hoặc DTT). Biến phụ thuộc là Defect Detection
Rate (DDR), hiệu quả trên mỗi test case, DDR theo loại lỗi, overlap, số lỗi chỉ
một kỹ thuật phát hiện và hiệu quả kết hợp.

Ba suite được thiết kế từ cùng một tài liệu business rules, sau đó đóng băng ở
Frozen v1.0 trước khi xem kết quả mutant. Baseline gồm EP 30 case, BVA 51 case và
DTT 29 case, tổng cộng 110 test ID duy nhất. File manifest được bảo vệ bởi SHA-256
`5cbd9e3b0e0b1aa0ef5e9f549eb09e0709fbb3093eccbff14a4c9ce24d8a9131` và Git
tag `frozen-v1.0` tại commit `431bcf8`.

Một Selenium runner dùng chung thực hiện cả ba suite trên cùng giao diện. Việc
dùng cùng runner, browser mode, selectors và assertion mechanism giúp giảm sai
lệch triển khai giữa các kỹ thuật.

## Dataset và mutant design

Dataset tự xây gồm ba form và 18 single-fault mutants. Mỗi mutant chỉ sửa một
biểu thức so với golden; tập mutant cân bằng 6 Partition, 6 Boundary và 6
Decision-rule defects, đồng thời cân bằng 6 mutant cho mỗi form.

| Mutant | Form | Category | Lỗi được gieo |
|---|---|---|---|
| M01 | Registration | Partition | Email không còn bắt buộc dấu chấm ở domain |
| M02 | Registration | Partition | Chấp nhận tuổi không nguyên |
| M03 | Registration | Boundary | Loại username đúng 5 ký tự |
| M04 | Registration | Boundary | Loại tuổi đúng 60 |
| M05 | Registration | Decision-rule | Bỏ điều kiện password confirmation khỏi quyết định |
| M06 | Registration | Decision-rule | Dùng AND thay OR cho khoảng username không hợp lệ |
| M07 | Shipping | Partition | Chấp nhận customer type lạ |
| M08 | Shipping | Partition | Chấp nhận region lạ |
| M09 | Shipping | Boundary | Coupon dùng `> 500,000` thay vì `>=` |
| M10 | Shipping | Boundary | Free shipping dùng `> 800,000` thay vì `>=` |
| M11 | Shipping | Decision-rule | Điều kiện VIP dùng OR thay AND |
| M12 | Shipping | Decision-rule | Cộng hai discount thay vì lấy mức lớn nhất |
| M13 | Loan | Partition | Chấp nhận tuổi không nguyên |
| M14 | Loan | Partition | Chấp nhận credit score không nguyên |
| M15 | Loan | Boundary | Thu nhập tối thiểu dùng `>` thay vì `>=` |
| M16 | Loan | Boundary | Khoản vay tối đa dùng `<` thay vì `<=` |
| M17 | Loan | Decision-rule | Bỏ điều kiện employment |
| M18 | Loan | Decision-rule | Điều kiện khoản vay dùng AND thay OR |

Mỗi mutant được xác minh theo hai tầng: file sinh ra phải bằng source golden cộng
đúng một replacement đã đăng ký; và output phải khác golden trên ít nhất một
frozen witness input. Cả 18 mutant đều hợp lệ và không tương đương theo tiêu chí
này.

## Experimental procedure

1. Kiểm tra fingerprint của Frozen v1.0.
2. Chạy EP, BVA và DTT trên golden. Điều kiện mở cổng là 30/30, 51/51 và 29/29.
3. Với từng M01–M18, chạy riêng ba suite bằng cùng Selenium runner.
4. Ghi `1` khi suite có assertion failure trên mutant và `0` khi toàn bộ suite
   pass. Lượt thiếu test, có setup/collection error hoặc skipped test được đánh
   dấu invalid và không được tính killed.
5. Tính metrics trực tiếp từ mutation matrix bằng script, không nhập tay.

Run ngày 14/08/2026 tạo đủ 57 báo cáo JUnit (golden và 18 mutant, mỗi phiên bản
ba suite). Golden đạt EP 30/30, BVA 51/51 và DTT 29/29. Không có lượt invalid.

DDR và efficiency được tính như sau:

\[
DDR = \frac{\text{Mutants killed}}{\text{Valid mutants}} \times 100\%
\]

\[
Efficiency = \frac{\text{Mutants killed}}{\text{Number of test cases}}
\]

## Results

### Mutation matrix

| Mutant | Category | EP | BVA | DTT |
|---|---|---:|---:|---:|
| M01 | Partition | 0 | 0 | 1 |
| M02 | Partition | 1 | 0 | 0 |
| M03 | Boundary | 0 | 1 | 0 |
| M04 | Boundary | 0 | 1 | 0 |
| M05 | Decision-rule | 1 | 0 | 1 |
| M06 | Decision-rule | 1 | 1 | 1 |
| M07 | Partition | 1 | 0 | 0 |
| M08 | Partition | 1 | 0 | 0 |
| M09 | Boundary | 0 | 1 | 0 |
| M10 | Boundary | 0 | 1 | 0 |
| M11 | Decision-rule | 0 | 1 | 1 |
| M12 | Decision-rule | 1 | 0 | 1 |
| M13 | Partition | 1 | 0 | 0 |
| M14 | Partition | 1 | 0 | 0 |
| M15 | Boundary | 0 | 1 | 0 |
| M16 | Boundary | 0 | 1 | 0 |
| M17 | Decision-rule | 1 | 0 | 1 |
| M18 | Decision-rule | 1 | 1 | 1 |

### Overall DDR và efficiency

| Suite | Test cases | Killed / 18 | DDR | Efficiency |
|---|---:|---:|---:|---:|
| EP | 30 | 10 | 55.56% | 0.3333 |
| BVA | 51 | 9 | 50.00% | 0.1765 |
| DTT | 29 | 7 | 38.89% | 0.2414 |

### DDR theo loại lỗi

| Suite | Partition (6) | Boundary (6) | Decision-rule (6) |
|---|---:|---:|---:|
| EP | 5/6 (83.33%) | 0/6 (0%) | 5/6 (83.33%) |
| BVA | 0/6 (0%) | 6/6 (100%) | 3/6 (50%) |
| DTT | 1/6 (16.67%) | 0/6 (0%) | 6/6 (100%) |

### Overlap, unique kills và combined effectiveness

EP–BVA cùng phát hiện 2 mutant (M06, M18), EP–DTT cùng phát hiện 5 mutant
(M05, M06, M12, M17, M18), còn BVA–DTT cùng phát hiện 3 mutant (M06, M11,
M18). Nếu tính Jaccard trên tập mutant killed, ba mức tương ứng là 11.76%,
41.67% và 23.08%.

EP có 5 unique kills; BVA có 6; DTT có 1. Hợp ba tập killed phát hiện 18/18
mutant, tức combined DDR đạt 100%, cao hơn EP 55.56%, BVA 50.00% và DTT 38.89%.

## Discussion

Kết quả ủng hộ ba kỳ vọng theo loại lỗi. EP mạnh nhất với Partition defects
(83.33% so với 0% và 16.67%). BVA mạnh nhất với Boundary defects (100% so với
0% của hai suite còn lại). DTT mạnh nhất với Decision-rule defects (100% so với
83.33% của EP và 50% của BVA).

EP có overall DDR và efficiency cao nhất trong benchmark này. Tuy nhiên không
nên diễn giải rằng EP luôn tốt nhất: EP cũng phát hiện nhiều decision-rule mutant
vì một số representative input của EP đồng thời kích hoạt rule combinations.
Tương tự, BVA phát hiện ba decision-rule mutant do các boundary case liên quan
đến quyết định tổng hợp. Đây là overlap tự nhiên giữa input domain và business
rules, không phải bằng chứng rằng các kỹ thuật tương đương nhau.

Kết quả quan trọng nhất là tính bổ sung. Không suite riêng nào vượt 10/18, trong
khi hợp ba suite đạt 18/18. Đặc biệt, sáu boundary mutants chỉ BVA phát hiện cho
thấy bỏ BVA sẽ tạo một khoảng trống lớn dù EP có overall DDR cao hơn. Vì vậy với
web-form business logic, chiến lược thực tế phù hợp là phối hợp EP để phủ input
classes, BVA để đánh vào ngưỡng và DTT để phủ tổ hợp điều kiện/quyết định.

Efficiency ở đây là số mutant killed trên số test case, không phải thời gian thực
thi và cũng chưa điều chỉnh theo độ khó của mutant. Do kích thước suite khác nhau,
chỉ số này nên được đọc cùng DDR theo category và unique kills.

## Threats to validity

- **Construct validity:** mutation score là proxy cho khả năng phát hiện lỗi,
  không đồng nhất hoàn toàn với defect detection trên lỗi sản xuất thực tế.
- **Internal validity:** nhóm tự xây requirements, suite và mutant nên có nguy
  cơ thiên lệch của người nghiên cứu. Freeze-before-mutation, fingerprint và
  witness verification giúp giảm nhưng không loại bỏ nguy cơ này.
- **External validity:** chỉ có ba form nhỏ viết bằng JavaScript thuần; chưa thể
  khái quát trực tiếp sang ứng dụng lớn, framework khác hoặc lỗi UI/UX phức tạp.
- **Conclusion validity:** chỉ có 18 mutant và mỗi category 6 mẫu; đây là pilot
  study mô tả, chưa đủ power cho kết luận thống kê mạnh. Các mutant cũng không
  phải mẫu ngẫu nhiên từ quần thể lỗi.
- **Test-suite size:** EP, BVA và DTT có số case khác nhau. Overall DDR có lợi cho
  suite lớn/rộng hơn, còn efficiency có thể ưu tiên suite nhỏ; cần đọc cả hai.
- **Mutant independence:** mỗi file là single-fault, nhưng vài lỗi có thể được
  nhiều loại input kích hoạt, làm xuất hiện overlap giữa kỹ thuật.

## Conclusion

Trong controlled benchmark này, kỹ thuật test ảnh hưởng rõ đến loại defect được
phát hiện. EP mạnh nhất với Partition, BVA đạt 100% Boundary DDR và DTT đạt 100%
Decision-rule DDR. EP đạt overall DDR cao nhất (55.56%) và efficiency cao nhất
(0.3333), nhưng không kỹ thuật nào riêng lẻ phát hiện quá 10/18 mutant. Kết hợp
cả ba đạt 18/18 (100%), xác nhận rằng EP, BVA và DTT bổ sung cho nhau trong kiểm
thử web-form business logic. Kết luận nên được xem là bằng chứng pilot và cần
lặp lại trên nhiều ứng dụng cùng defect thực tế hơn.

## Reproducibility artifacts

- Frozen definition: `test-design/FROZEN-v1.0.md`
- Frozen test data: `tests/frozen_cases.py`
- Mutant catalog and witness outputs: `mutant-manifest.json`
- Selenium runner: `tests/selenium/form_runner.py`
- Experiment runner: `scripts/run_experiment.py`
- Raw matrix: `experiment-results/frozen-v1.0-run-20260814/mutation-matrix.csv`
- Calculated metrics: `experiment-results/frozen-v1.0-run-20260814/metrics.json`
- Per-run evidence: `experiment-results/frozen-v1.0-run-20260814/junit/`
