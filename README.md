# Kiểm thử tự động Selenium: saucedemo.com

## 1. Giới thiệu

Dự án thực hành kiểm thử tự động giao diện web bằng **Selenium 4** và **pytest**, trên trang demo mua hàng [saucedemo.com](https://www.saucedemo.com/). Dự án gồm 6 test case bao phủ chức năng đăng nhập, thêm sản phẩm vào giỏ hàng và đăng xuất.

## 2. Môi trường thực hiện

| Thành phần | Phiên bản / Ghi chú |
|------------|---------------------|
| Ngôn ngữ | Python 3.13 |
| Thư viện kiểm thử | Selenium 4, pytest 8.4.2, pytest-html |
| Trình duyệt | Google Chrome 156 (chạy headless) |
| Nền tảng chạy | Google Colab |
| Hệ điều hành | Ubuntu 24.04 (runtime Colab) |

## 3. Danh sách test case

| ID | Tên test case | Các bước | Kết quả mong đợi | Kết quả thực tế |
|----|---------------|----------|------------------|-----------------|
| TC01 | Đăng nhập thành công | Nhập standard_user / secret_sauce, nhấn Login | Chuyển sang trang Products | Pass |
| TC02 | Sai mật khẩu | Nhập standard_user / wrong_password | Hiện thông báo "Username and password do not match" | Pass |
| TC03 | Tài khoản bị khóa | Nhập locked_out_user / secret_sauce | Hiện thông báo "locked out" | Pass |
| TC04 | Bỏ trống username | Để trống username, nhập password | Hiện thông báo "Username is required" | Pass |
| TC05 | Thêm sản phẩm vào giỏ | Đăng nhập, nhấn Add to cart sản phẩm Sauce Labs Backpack | Nút đổi thành Remove, badge giỏ hàng hiện "1" | Pass |
| TC06 | Đăng xuất | Đăng nhập, mở menu, nhấn Logout | Quay về trang đăng nhập | Pass |

## 4. Cách cài đặt và chạy test

```bash
pip install -r requirements.txt
python -m pytest -v
```

Tạo báo cáo HTML:

```bash
python -m pytest -v --html=report.html --self-contained-html
```

Lưu ý: fixture hiện dùng `binary_location = "/usr/bin/google-chrome"` (môi trường Colab). Khi chạy trên máy Windows, xóa dòng đó để Selenium tự tìm Chrome đã cài.

## 5. Kết quả thực thi

```
test_saucedemo.py::test_tc01_login_success PASSED
test_saucedemo.py::test_tc02_login_wrong_password PASSED
test_saucedemo.py::test_tc03_login_locked_out_user PASSED
test_saucedemo.py::test_tc04_login_empty_username PASSED
test_saucedemo.py::test_tc05_add_product_to_cart PASSED
test_saucedemo.py::test_tc06_logout PASSED

6 passed
```

Báo cáo chi tiết: [report.html](report.html)

## 6. Ghi chú kỹ thuật

- **Chờ đợi tường minh:** các test dùng `WebDriverWait` với `expected_conditions` thay cho `time.sleep()`, nên chỉ chờ đúng khi cần.
- **Click bằng JavaScript:** trang saucedemo được xây bằng React, render bất đồng bộ. Một số nút (thêm giỏ hàng, menu, Logout) dễ bị che hoặc chưa sẵn sàng khi headless, nên dùng `execute_script` để click.
- **Kiểm tra theo trạng thái:** TC05 chờ nút đổi thành "Remove" và badge hiện "1" thay vì chỉ chờ badge xuất hiện.
- **Độc lập giữa các test:** mỗi test mở một trình duyệt mới qua fixture `driver` và đóng sau khi xong.

## 7. Hạn chế và hướng phát triển

- Chỉ kiểm thử luồng chính, chưa có test sắp xếp sản phẩm, thanh toán hay xóa sản phẩm khỏi giỏ.
- Dữ liệu đăng nhập đang viết cứng trong code. Có thể chuyển sang `@pytest.mark.parametrize` để gộp TC02–TC04.
- Có thể áp dụng Page Object Model để tách locator khỏi logic test.
