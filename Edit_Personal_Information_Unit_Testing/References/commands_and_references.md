# TÀI LIỆU THAM KHẢO VÀ DANH SÁCH CÂU LỆNH KIỂM THỬ

**Chức năng:** Edit Personal Information / Edit Profile  
**Dự án:** Hệ thống Quản lý Rạp chiếu phim (Cinema Management System)  
**Môn học:** Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)  

---

## 1. Danh sách câu lệnh thực thi kiểm thử (Test Execution Commands)

### 1.1. Chạy toàn bộ 22 Unit Test cho Edit Personal Information
```bash
# Di chuyển vào thư mục auth-service (nơi cài đặt Jest test runner)
cd auth-service

# Thực thi kiểm thử đơn vị
npx jest --config jest.editProfile.config.cjs src/__tests__/userController.editProfile.test.ts
```

### 1.2. Chạy kiểm thử kèm đo độ bao phủ mã nguồn (Code Coverage Report)
```bash
# Đo Statement và Branch Coverage trên userController và userService
npx jest --config jest.editProfile.config.cjs --coverage
```

### 1.3. Chạy riêng nhóm kiểm thử Kiểm tra CSDL (CheckDB & Rollback)
```bash
# Lọc test suite nhóm CheckDB & Rollback
npx jest --config jest.editProfile.config.cjs -t "CheckDB và Rollback giao dịch"
```

### 1.4. Sinh lại file Excel Test Cases và Báo cáo tự động
```bash
# Từ thư mục gốc dự án
python create_edit_profile_excel.py
```

### 1.5. Tạo lại ảnh chụp màn hình minh chứng
```bash
# Từ thư mục gốc dự án
python generate_edit_profile_screenshots.py
```

---

## 2. Tài liệu tham khảo học thuật (Academic References)

1. **Giáo trình Kiểm thử phần mềm:**
   - **Mục 5.3:** Xây dựng bộ test case cho kiểm thử đơn vị (Bảng ma trận: TT, Chức năng/Use case, Lớp điều khiển, Phương thức, Trường hợp test).
   - **Mục 5.3.2:** Cài đặt kiểm thử đơn vị:
     * Bước 1: Xây dựng test cases đạt mức phủ cấp 2 (C2 branch coverage - phủ hết các nhánh trong source code).
     * Bước 2: Viết script test: khai báo input/expected, gọi method cần test, kiểm tra kết quả thực method với expected output, **kiểm tra DB (CheckDB)** xem đã thay đổi như mong muốn chưa.
     * Bước 3: Báo cáo kết quả test, số lượng pass/fail và mô tả trường hợp.
     * **Cơ chế Rollback:** Chuẩn bị môi trường và rollback sau khi test để đảm bảo CSDL nguyên vẹn, không để lại dữ liệu rác.
2. **Jest Documentation (v29.7):** https://jestjs.io/docs/getting-started
3. **Istanbul Code Coverage Tool:** https://istanbul.js.org/
4. **Sequelize ORM Testing Best Practices:** https://sequelize.org/docs/v6/getting-started/
