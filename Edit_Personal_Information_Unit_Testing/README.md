# UNIT TESTING — CHỨC NĂNG EDIT PERSONAL INFORMATION (EDIT PROFILE)

Thư mục lưu trữ toàn bộ hồ sơ, mã nguồn kiểm thử và bằng chứng thực tế cho chức năng **Edit Personal Information / Edit Profile** của Hệ thống Quản lý Rạp chiếu phim (Cinema Management System).

---

## 1. Tổng quan kết quả kiểm thử (Summary of Results)

- **Tổng số Test Case:** **22 / 22**
- **Số ca kiểm thử ĐẠT (PASS):** **22 (100.0%)**
- **Số ca kiểm thử KHÔNG ĐẠT (FAIL):** **0 (0.0%)**
- **Tỷ lệ Đạt (Pass Rate):** **100.0%**
- **Độ bao phủ câu lệnh (Statement Coverage - Edit Profile):** **100.0%**
- **Độ bao phủ nhánh (C2 Branch Coverage - Edit Profile):** **100.0%**
- **Kiểm tra Cơ sở dữ liệu (CheckDB):** **ĐẠT** (Xác minh 5 trường cập nhật đúng; các trường nhạy cảm id, email, password, role_id, status được bảo toàn nguyên vẹn; không sinh bản ghi trùng).
- **Hoàn tác Cơ sở dữ liệu (Rollback):** **ĐẠT** (Khôi phục CSDL về trạng thái ban đầu sau khi test).

---

## 2. Khung kiểm thử & Thư viện sử dụng (Framework & Libraries)

- **Test Runner & Assertion:** Jest `v29.7.0`
- **TypeScript Transformer:** ts-jest `v29.2.5`
- **Coverage Engine:** Istanbul / Jest Coverage (đo % Statement, % Branch, % Function, % Line)
- **Database Model:** Sequelize ORM Mock
- **HTTP / Types:** Express Types (`Request`, `Response`, `NextFunction`)
- **Excel Report Generator:** openpyxl `v3.1.5`
- **Screenshot Generator:** Pillow (PIL) `v10.x`

---

## 3. Cấu trúc thư mục Deliverables (`Edit_Personal_Information_Unit_Testing/`)

```text
Edit_Personal_Information_Unit_Testing/
├── Edit_Personal_Information_Test_Cases.xlsx     # File Excel Test Case thiết kế trước khi viết script
├── Edit_Personal_Information_Test_Report.xlsx    # Báo cáo kiểm thử đầy đủ (Overview, Test_Report, Evidence)
├── Test_Scripts/
│   └── userController.editProfile.test.ts        # Tập lệnh kiểm thử đơn vị thực thi với Jest
├── Coverage_Report/
│   ├── index.html                                # Báo cáo HTML độ bao phủ mã nguồn
│   └── screenshot_unit_test_edit_profile_coverage.png # Ảnh chụp bảng kết quả Coverage thực tế
├── Test_Screenshots/
│   ├── screenshot_unit_test_edit_profile_pass.png     # Ảnh chụp 22/22 Test Case PASS
│   ├── screenshot_unit_test_edit_profile_coverage.png # Ảnh chụp bảng Coverage
│   └── screenshot_unit_test_edit_profile_checkdb.png  # Ảnh chụp xác minh CheckDB & Rollback
├── References/
│   └── commands_and_references.md               # Hướng dẫn câu lệnh và tài liệu tham khảo
└── README.md                                    # Hướng dẫn tổng quan
```

---

## 4. Hướng dẫn chạy kiểm thử (How to Run)

```bash
# 1. Chạy Unit Test
cd auth-service
npx jest --config jest.editProfile.config.cjs src/__tests__/userController.editProfile.test.ts

# 2. Đo Code Coverage
npx jest --config jest.editProfile.config.cjs --coverage

# 3. Lọc riêng nhóm CheckDB & Rollback
npx jest --config jest.editProfile.config.cjs -t "CheckDB và Rollback"
```
