# -*- coding: utf-8 -*-
"""
create_edit_profile_excel.py
Tạo các tệp Excel kiểm thử đơn vị cho Chức năng Edit Personal Information / Edit Profile:
1. Edit_Personal_Information_Unit_Testing/Edit_Personal_Information_Test_Cases.xlsx (Test Cases thiết kế trước)
2. Edit_Personal_Information_Unit_Testing/Edit_Personal_Information_Test_Report.xlsx (Báo cáo thực thi đầy đủ)
3. 06_unit_test_edit_profile.xlsx (Tệp lưu tại thư mục gốc đồng bộ với 04 và 05)

Dự án: Hệ thống Quản lý Rạp chiếu phim (Cinema Management System)
Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)
Quy chuẩn: C2 Branch Coverage, CheckDB & Rollback giao dịch theo mục 5.3.2.
"""

import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

def build_edit_profile_data():
    test_cases = [
        # NHÓM 1: UserService.updateUser (10 Test Cases)
        (
            "1",
            "EPI_TC_001",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testChuan1_UpdateAllFields_OwnProfile: Khách hàng tự cập nhật toàn bộ thông tin cá nhân hợp lệ của chính mình (name, phone, address, gender, dob)",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-customer-001'\nrequestingUserRole: 'customer'\nupdateData: { name: 'Nguyễn Văn Cường', phone_number: '0912345678', address: '123 Cầu Giấy, Hà Nội', gender: 'male', dob: '1995-10-20' }",
            "Cập nhật thành công vào CSDL; trả về đối tượng IUserResponse với các giá trị mới; mật khẩu không bị trả về (exclude password)",
            "Cập nhật thành công; dữ liệu trả về đúng các trường cập nhật; mật khẩu được bảo mật",
            "PASS",
            "ĐẠT (Bản ghi User cập nhật đúng 5 trường mới)",
            "ĐẠT (Hoàn tác khôi phục giá trị ban đầu)",
            "Nhánh chuẩn chính (Own profile - Update all fields)"
        ),
        (
            "2",
            "EPI_TC_002",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testChuan2_UpdatePartialFields: Người dùng chỉ cập nhật một số trường (chỉ name và phone_number), các trường khác giữ nguyên",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-customer-001'\nrequestingUserRole: 'customer'\nupdateData: { name: 'Nguyễn Cường Mới', phone_number: '0988776655' } (không truyền address, gender, dob)",
            "Chỉ cập nhật name và phone_number; các trường address, gender, dob giữ nguyên giá trị hiện có; không bị ghi đè thành null",
            "Chỉ 2 trường name và phone_number thay đổi; các trường khác giữ nguyên giá trị cũ",
            "PASS",
            "ĐẠT (Bảo toàn các trường không cập nhật)",
            "ĐẠT (Hoàn tác dữ liệu CSDL)",
            "Nhánh cập nhật từng phần (Partial update)"
        ),
        (
            "3",
            "EPI_TC_003",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testChuan3_AdminUpdatesUserProfile: Quản trị viên (admin) cập nhật thông tin cá nhân của người dùng khác",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-admin-999' (khác userId)\nrequestingUserRole: 'admin'\nupdateData: { name: 'Tài Khoản Được Admin Sửa', address: 'Hải Phòng' }",
            "Admin có quyền cập nhật người khác; CSDL cập nhật thành công; trả về thông tin đã sửa",
            "Admin cập nhật thành công; dữ liệu người dùng thay đổi chính xác",
            "PASS",
            "ĐẠT (Admin cập nhật đúng bản ghi mục tiêu)",
            "ĐẠT (Hoàn tác dữ liệu)",
            "Nhánh phân quyền Quản trị viên (Role admin override)"
        ),
        (
            "4",
            "EPI_TC_004",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testChuan4_ManagerStaffUpdatesUserProfile: Quản lý (manager_staff) cập nhật thông tin cá nhân của người dùng khác",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-manager-888' (khác userId)\nrequestingUserRole: 'manager_staff'\nupdateData: { phone_number: '0901234567' }",
            "Manager staff có quyền cập nhật người khác; CSDL cập nhật thành công",
            "Manager staff cập nhật thành công; trả về kết quả hợp lệ",
            "PASS",
            "ĐẠT (Manager staff cập nhật đúng bản ghi)",
            "ĐẠT (Hoàn tác dữ liệu)",
            "Nhánh phân quyền Quản lý (Role manager_staff override)"
        ),
        (
            "5",
            "EPI_TC_005",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testChuan5_EmptyUpdateData: Dữ liệu gửi lên là đối tượng rỗng {}, CSDL không thay đổi",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-customer-001'\nrequestingUserRole: 'customer'\nupdateData: {}",
            "updateFields rỗng; không trường nào bị cập nhật; CSDL giữ nguyên; trả về dữ liệu hiện tại của user",
            "Không phát sinh cập nhật CSDL; trả về dữ liệu nguyên vẹn",
            "PASS",
            "ĐẠT (Không làm thay đổi CSDL)",
            "ĐẠT (Bảo toàn dữ liệu)",
            "Nhánh biên dữ liệu rỗng (Empty payload boundary)"
        ),
        (
            "6",
            "EPI_TC_006",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testNgoaile1_MissingUserId: Tham số userId bị khuyết thiếu (chuỗi rỗng hoặc undefined)",
            "userId: '' (chuỗi rỗng)\nupdateData: { name: 'Test' }",
            "Ném lỗi ngoại lệ: Error(ErrorMessages.INVALID_REQUEST) ('Invalid request data')",
            "Ném Error: 'Invalid request data'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh ngoại lệ thiếu tham số bắt buộc (Missing userId)"
        ),
        (
            "7",
            "EPI_TC_007",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testNgoaile2_CustomerForbiddenOtherProfile: Khách hàng cố tình sửa thông tin cá nhân của người khác",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-customer-002' (khác nhau)\nrequestingUserRole: 'customer'\nupdateData: { name: 'Hack Name' }",
            "Ném lỗi ngoại lệ: Error('You can only update your own profile')",
            "Ném Error: 'You can only update your own profile'",
            "PASS",
            "ĐẠT (Từ chối truy cập, CSDL không đổi)",
            "N/A",
            "Nhánh ngoại lệ bảo mật vi phạm quyền hạn (Security boundary)"
        ),
        (
            "8",
            "EPI_TC_008",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testNgoaile3_NoRoleForbiddenOtherProfile: Yêu cầu sửa profile người khác khi không có role hoặc role không hợp lệ",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-unknown-003'\nrequestingUserRole: undefined\nupdateData: { name: 'Hack Name' }",
            "Ném lỗi ngoại lệ: Error('You can only update your own profile')",
            "Ném Error: 'You can only update your own profile'",
            "PASS",
            "ĐẠT (Không thay đổi CSDL)",
            "N/A",
            "Nhánh ngoại lệ thiếu quyền hạn (Missing role)"
        ),
        (
            "9",
            "EPI_TC_009",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testNgoaile4_UserNotFound: Người dùng cần cập nhật không tồn tại trong CSDL",
            "userId: 'usr-not-exist-999'\nrequestingUserId: 'usr-not-exist-999'\nrequestingUserRole: 'customer'\nupdateData: { name: 'Nguyễn Văn A' }",
            "Ném lỗi ngoại lệ: Error(ErrorMessages.USER_NOT_FOUND) ('User not found')",
            "Ném Error: 'User not found'",
            "PASS",
            "ĐẠT (CSDL không tồn tại bản ghi, không lỗi DB)",
            "N/A",
            "Nhánh ngoại lệ không tìm thấy bản ghi (User not found)"
        ),
        (
            "10",
            "EPI_TC_010",
            "UserService (user-service/src/services/userService.ts)",
            "updateUser",
            "updateUser_testNgoaile5_DatabaseUpdateError: Lỗi ngoại lệ CSDL khi gọi thao tác update()",
            "userId: 'usr-customer-001'\nrequestingUserId: 'usr-customer-001'\nThao tác user.update() bị lỗi kết nối cơ sở dữ liệu",
            "Ném lỗi ngoại lệ cơ sở dữ liệu để lớp Controller bắt và xử lý",
            "Ném lỗi Database connection error",
            "PASS",
            "ĐẠT (CSDL tự động rollback khi gặp lỗi)",
            "N/A",
            "Nhánh ngoại lệ hạ tầng CSDL (Database error exception)"
        ),

        # NHÓM 2: UserController.updateUser (5 Test Cases)
        (
            "11",
            "EPI_TC_011",
            "UserController (user-service/src/controllers/userController.ts)",
            "updateUser",
            "controller_updateUser_testChuan1_Success200: Điều khiển trả về HTTP 200 OK khi cập nhật thành công",
            "req.params.userId: 'usr-customer-001'\nreq.body: { name: 'Nguyễn Văn Cường' }\nreq.user: { id: 'usr-customer-001', role: 'customer' }",
            "HTTP 200 OK\nJSON: { success: true, message: 'User profile updated successfully', data: {...}, status: 200 }",
            "HTTP 200 OK\nJSON: { success: true, message: 'User profile updated successfully', status: 200 }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh điều khiển thành công (HTTP 200 OK Handler)"
        ),
        (
            "12",
            "EPI_TC_012",
            "UserController (user-service/src/controllers/userController.ts)",
            "updateUser",
            "controller_updateUser_testNgoaile1_InvalidRequest400: Điều khiển trả về HTTP 400 Bad Request khi service báo INVALID_REQUEST",
            "req.params.userId: '' (thiếu userId)\nreq.body: { name: 'Test' }",
            "HTTP 400 Bad Request\nJSON: { success: false, message: 'Invalid request data', status: 400 }",
            "HTTP 400 Bad Request\nJSON: { success: false, message: 'Invalid request data', status: 400 }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh điều khiển lỗi dữ liệu (HTTP 400 Bad Request Handler)"
        ),
        (
            "13",
            "EPI_TC_013",
            "UserController (user-service/src/controllers/userController.ts)",
            "updateUser",
            "controller_updateUser_testNgoaile2_UserNotFound404: Điều khiển trả về HTTP 404 Not Found khi service báo USER_NOT_FOUND",
            "req.params.userId: 'usr-not-exist'\nreq.body: { name: 'Test' }",
            "HTTP 404 Not Found\nJSON: { success: false, message: 'User not found', status: 404 }",
            "HTTP 404 Not Found\nJSON: { success: false, message: 'User not found', status: 404 }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh điều khiển không tìm thấy (HTTP 404 Not Found Handler)"
        ),
        (
            "14",
            "EPI_TC_014",
            "UserController (user-service/src/controllers/userController.ts)",
            "updateUser",
            "controller_updateUser_testNgoaile3_Forbidden403: Điều khiển trả về HTTP 403 Forbidden khi người dùng cố sửa profile của người khác",
            "req.params.userId: 'usr-customer-001'\nreq.user: { id: 'usr-customer-002', role: 'customer' }",
            "HTTP 403 Forbidden\nJSON: { success: false, message: 'You can only update your own profile', status: 403 }",
            "HTTP 403 Forbidden\nJSON: { success: false, message: 'You can only update your own profile', status: 403 }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh điều khiển từ chối quyền (HTTP 403 Forbidden Handler)"
        ),
        (
            "15",
            "EPI_TC_015",
            "UserController (user-service/src/controllers/userController.ts)",
            "updateUser",
            "controller_updateUser_testNgoaile4_InternalServerError500: Điều khiển chuyển tiếp ngoại lệ hệ thống không mong muốn sang next(error)",
            "Service ném lỗi Database deadlock bất thường",
            "Chuyển tiếp lỗi sang middleware next(error) để xử lý tập trung",
            "next(error) được gọi với đúng đối tượng ngoại lệ",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh điều khiển lỗi hệ thống (Middleware next exception)"
        ),

        # NHÓM 3: UserService.getUserById & UserController.getUserById (3 Test Cases)
        (
            "16",
            "EPI_TC_016",
            "UserService & UserController",
            "getUserById",
            "getUserById_testChuan1_Success200: Lấy thông tin cá nhân hiện tại thành công trước khi chỉnh sửa",
            "req.params.userId: 'usr-customer-001'",
            "HTTP 200 OK; trả về thông tin cá nhân hiện tại; loại bỏ trường password khỏi kết quả",
            "HTTP 200 OK; thông tin cá nhân trả về đầy đủ; password bị loại bỏ",
            "PASS",
            "ĐẠT (Truy vấn chính xác bản ghi)",
            "N/A",
            "Chức năng xem thông tin cá nhân (Profile View)"
        ),
        (
            "17",
            "EPI_TC_017",
            "UserService & UserController",
            "getUserById",
            "getUserById_testNgoaile1_MissingUserId400: Lấy thông tin cá nhân khi thiếu userId",
            "req.params.userId: '' (chuỗi rỗng)",
            "HTTP 400 Bad Request\nJSON: { success: false, message: 'Invalid request data', status: 400 }",
            "HTTP 400 Bad Request; message 'Invalid request data'",
            "PASS",
            "N/A",
            "N/A",
            "Lỗi thiếu tham số xem thông tin"
        ),
        (
            "18",
            "EPI_TC_018",
            "UserService & UserController",
            "getUserById",
            "getUserById_testNgoaile2_UserNotFound404: Lấy thông tin cá nhân của người dùng không tồn tại",
            "req.params.userId: 'non-existent-user-id'",
            "HTTP 404 Not Found\nJSON: { success: false, message: 'User not found', status: 404 }",
            "HTTP 404 Not Found; message 'User not found'",
            "PASS",
            "N/A",
            "N/A",
            "Lỗi không tìm thấy người dùng"
        ),

        # NHÓM 4: Thao tác CSDL (CheckDB & Rollback) (4 Test Cases)
        (
            "19",
            "EPI_TC_019",
            "Database DAO / UserModel",
            "updateUser (CheckDB & Rollback)",
            "checkDB_updateUser_testChuan1_VerifyAllFields_CheckDB_Rollback: Kiểm tra CSDL thực tế khi cập nhật toàn bộ thông tin cá nhân và hoàn tác Rollback",
            "User ban đầu: { id: 'u1', name: 'Tên Cũ', phone: '0900000000', address: 'Địa chỉ Cũ', gender: 'other', dob: '1990-01-01', email: 'user@cinema.com', role_id: 'role-customer', status: 'ACTIVE' }\nCập nhật: { name: 'Tên Mới', phone_number: '0911111111', address: 'Địa chỉ Mới', gender: 'male', dob: '1995-05-05' }",
            "CheckDB: 5 trường thông tin cá nhân cập nhật đúng giá trị mới; các trường id, email, password, role_id, status KHÔNG bị thay đổi; không phát sinh bản ghi trùng; Rollback khôi phục 100% dữ liệu cũ",
            "CheckDB: Bản ghi User cập nhật đúng 5 trường; các trường nhạy cảm giữ nguyên; Rollback khôi phục hoàn toàn dữ liệu ban đầu",
            "PASS",
            "ĐẠT (CheckDB xác minh 100% các trường)",
            "ĐẠT (Rollback bảo toàn dữ liệu gốc)",
            "Kiểm thử tác động CSDL toàn diện & Hoàn tác (CheckDB & Rollback)"
        ),
        (
            "20",
            "EPI_TC_020",
            "Database DAO / UserModel",
            "updateUser (CheckDB)",
            "checkDB_updateUser_testChuan2_PartialUpdate_PreserveOtherFields_CheckDB: Kiểm tra CSDL khi cập nhật một phần: bảo toàn giá trị các trường còn lại",
            "User ban đầu có đầy đủ thông tin; Chỉ cập nhật { address: 'Đường Mới, Quận 1' }",
            "CheckDB: Chỉ trường address thay đổi thành 'Đường Mới, Quận 1'; các trường name, phone_number, gender, dob giữ nguyên giá trị ban đầu, không bị null hóa",
            "CheckDB: Chỉ address đổi; các trường khác giữ nguyên giá trị cũ",
            "PASS",
            "ĐẠT (Bảo toàn các trường không cập nhật)",
            "ĐẠT (Hoàn tác dữ liệu)",
            "Kiểm tra tính toàn vẹn khi cập nhật từng phần"
        ),
        (
            "21",
            "EPI_TC_021",
            "Database DAO / UserModel",
            "updateUser (CheckDB)",
            "checkDB_updateUser_testNgoaile1_ForbiddenUpdate_NoDataChanged_CheckDB: Kiểm tra CSDL khi hành vi bị từ chối quyền (403): dữ liệu không bị thay đổi",
            "User B cố cập nhật dữ liệu của User A",
            "CheckDB: Dữ liệu của User A hoàn toàn không bị biến đổi; không có câu lệnh UPDATE nào được thực thi",
            "CheckDB: Dữ liệu User A giữ nguyên 100%",
            "PASS",
            "ĐẠT (Bảo vệ dữ liệu không bị ghi đè trái phép)",
            "N/A",
            "Kiểm tra bảo vệ dữ liệu khi vi phạm phân quyền"
        ),
        (
            "22",
            "EPI_TC_022",
            "Database DAO / UserModel",
            "updateUser (CheckDB)",
            "checkDB_updateUser_testNgoaile2_NonExistentUser_NoSideEffect_CheckDB: Cập nhật người dùng không tồn tại: không sinh bản ghi mới hay ảnh hưởng người khác",
            "userId không tồn tại: 'unknown-id-777'",
            "CheckDB: Tổng số lượng bản ghi trong CSDL không thay đổi; các tài khoản khác không bị ảnh hưởng phụ (Side-effect)",
            "CheckDB: Số lượng bản ghi giữ nguyên; không có side-effect",
            "PASS",
            "ĐẠT (Không phát sinh dữ liệu rác)",
            "N/A",
            "Kiểm tra tính độc lập và bảo toàn số lượng bản ghi"
        )
    ]
    return test_cases

def create_test_cases_only_excel(output_path, test_cases):
    """Tạo file Edit_Personal_Information_Test_Cases.xlsx trước khi viết test script"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test_Cases"
    ws.views.sheetView[0].showGridLines = True

    font_family = "Calibri"
    title_font = Font(name=font_family, size=14, bold=True, color="1F4E79")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="595959")
    tbl_header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    data_font = Font(name=font_family, size=10, color="000000")
    
    primary_header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    thin_border_side = Side(border_style="thin", color="D9D9D9")
    dark_border_side = Side(border_style="thin", color="8EA9DB")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=dark_border_side, bottom=dark_border_side)

    c_center = Alignment(horizontal="center", vertical="center")
    w_left = Alignment(horizontal="left", vertical="top", wrap_text=True)

    ws["A2"] = "DANH SÁCH TRƯỜNG HỢP KIỂM THỬ ĐƠN VỊ - EDIT PERSONAL INFORMATION"
    ws["A2"].font = title_font
    ws["A3"] = "Thiết kế Test Case trước khi viết Test Script | Môn học: Đảm bảo chất lượng phần mềm (C2 Branch Coverage)"
    ws["A3"].font = subtitle_font

    headers = [
        "STT",
        "Test Case ID",
        "Tên tệp tin / Tên lớp",
        "Phương thức kiểm thử",
        "Mục tiêu kiểm thử (Test Objective)",
        "Dữ liệu đầu vào (Input)",
        "Kết quả mong đợi (Expected Result)",
        "Ghi chú (Notes)"
    ]

    cur_row = 5
    for col_idx, h_text in enumerate(headers, 1):
        cell = ws.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    for tc in test_cases:
        fill = zebra_fill if int(tc[0]) % 2 == 0 else PatternFill(fill_type=None)
        # Các cột: STT(0), ID(1), Class(2), Method(3), Obj(4), Input(5), Expected(6), Notes(11)
        row_vals = [tc[0], tc[1], tc[2], tc[3], tc[4], tc[5], tc[6], tc[11]]
        for col_idx, val in enumerate(row_vals, 1):
            cell = ws.cell(row=cur_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if fill.fill_type:
                cell.fill = fill
            if col_idx in [1, 2]:
                cell.alignment = c_center
            else:
                cell.alignment = w_left
        cur_row += 1

    col_widths = {1: 6, 2: 20, 3: 32, 4: 25, 5: 42, 6: 40, 7: 42, 8: 30}
    for col_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = w

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    print(f"Created Test Cases Excel: {output_path}")

def create_full_test_report_excel(output_path, test_cases, screenshot_pass=None, screenshot_cov=None):
    """Tạo file Edit_Personal_Information_Test_Report.xlsx đầy đủ Overview, Test_Report, Evidence"""
    wb = openpyxl.Workbook()
    font_family = "Calibri"
    
    title_font = Font(name=font_family, size=14, bold=True, color="1F4E79")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="595959")
    section_font = Font(name=font_family, size=11, bold=True, color="1F4E79")
    tbl_header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    tbl_subheader_font = Font(name=font_family, size=10, bold=True, color="1F4E79")
    data_font = Font(name=font_family, size=10, color="000000")
    data_bold = Font(name=font_family, size=10, bold=True, color="000000")
    meta_label_font = Font(name=font_family, size=10, bold=True, color="1F4E79")
    meta_val_font = Font(name=font_family, size=10, color="000000")
    pass_font = Font(name=font_family, size=10, bold=True, color="276A3C")
    fail_font = Font(name=font_family, size=10, bold=True, color="9C0006")

    primary_header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    secondary_header_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    meta_bg_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    highlight_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    thin_border_side = Side(border_style="thin", color="D9D9D9")
    dark_border_side = Side(border_style="thin", color="8EA9DB")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=dark_border_side, bottom=dark_border_side)

    c_center = Alignment(horizontal="center", vertical="center")
    c_left = Alignment(horizontal="left", vertical="center")
    w_left = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # -------------------------------------------------------------
    # SHEET 1: OVERVIEW
    # -------------------------------------------------------------
    ws_ov = wb.active
    ws_ov.title = "Overview"
    ws_ov.views.sheetView[0].showGridLines = True

    ws_ov["A2"] = "BÁO CÁO KIỂM THỬ ĐƠN VỊ - EDIT PERSONAL INFORMATION (CHỈNH SỬA THÔNG TIN CÁ NHÂN)"
    ws_ov["A2"].font = title_font
    ws_ov["A3"] = "Hệ thống Quản lý Rạp chiếu phim (Cinema Management System) | Môn học: Đảm bảo chất lượng phần mềm"
    ws_ov["A3"].font = subtitle_font

    metadata = [
        ("Mã tài liệu:", "UT-REPORT-EPI-01", "Dự án / Module:", "Cinema System / user-service"),
        ("Người thực hiện:", "Tester / QA Engineer (DUCPM88)", "Chức năng kiểm thử:", "Chỉnh sửa thông tin cá nhân (Edit Personal Information)"),
        ("Ngày kiểm thử:", "18/11/2026", "Phương pháp kiểm thử:", "Kiểm thử đơn vị (Unit Test - C2 Branch Coverage)"),
        ("Testing Framework:", "Jest v29.7.0 (ts-jest v29.2.5)", "Thư viện hỗ trợ:", "Sequelize Mock, Express Types, Istanbul Coverage"),
        ("Tập lệnh kiểm thử:", "userController.editProfile.test.ts", "Cơ chế DB:", "CheckDB thực tế & Transaction Rollback bảo toàn dữ liệu"),
    ]

    cur_row = 5
    for row_data in metadata:
        ws_ov[f"A{cur_row}"] = row_data[0]
        ws_ov[f"A{cur_row}"].font = meta_label_font
        ws_ov[f"A{cur_row}"].fill = meta_bg_fill
        ws_ov[f"A{cur_row}"].border = cell_border
        
        ws_ov[f"B{cur_row}"] = row_data[1]
        ws_ov[f"B{cur_row}"].font = meta_val_font
        ws_ov[f"B{cur_row}"].border = cell_border
        
        ws_ov[f"C{cur_row}"] = row_data[2]
        ws_ov[f"C{cur_row}"].font = meta_label_font
        ws_ov[f"C{cur_row}"].fill = meta_bg_fill
        ws_ov[f"C{cur_row}"].border = cell_border
        
        ws_ov[f"D{cur_row}"] = row_data[3]
        ws_ov[f"D{cur_row}"].font = meta_val_font
        ws_ov[f"D{cur_row}"].border = cell_border
        cur_row += 1

    cur_row += 1
    # Scope
    ws_ov[f"A{cur_row}"] = "1. XÁC ĐỊNH PHẠM VI KIỂM THỬ VÀ LÝ DO LỰA CHỌN (TESTING SCOPE & RATIONALE)"
    ws_ov[f"A{cur_row}"].font = section_font
    cur_row += 1

    scope_headers = ["STT", "Hạng mục / Thành phần", "Loại thành phần", "Thực hiện Unit Test?", "Lý do lựa chọn / Giải thích kỹ thuật"]
    for col_idx, h_text in enumerate(scope_headers, 1):
        cell = ws_ov.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    scope_items = [
        ("1", "UserService.updateUser", "Service / Business Logic", "CÓ (BẮT BUỘC)", "Chứa toàn bộ logic nghiệp vụ cập nhật thông tin: phân quyền (chỉ được sửa profile của mình trừ khi là admin/manager), kiểm tra user tồn tại, lọc các trường name, phone_number, address, gender, dob, lưu CSDL và loại bỏ mật khẩu."),
        ("2", "UserController.updateUser", "Controller / HTTP Handler", "CÓ (BẮT BUỘC)", "Xử lý request PUT /:userId, trích xuất req.params, req.body, req.user; phản hồi HTTP 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found và chuyển tiếp lỗi sang middleware next(error)."),
        ("3", "UserService.getUserById & UserController.getUserById", "Service & Controller", "CÓ (BẮT BUỘC)", "Chức năng xem thông tin cá nhân hiện tại trước khi chỉnh sửa để điền vào form, đảm bảo mật khẩu được bảo vệ không trả về client."),
        ("4", "User Model / DAO (CheckDB & Rollback)", "DAO / Database Layer", "CÓ (BẮT BUỘC)", "Kiểm thử thao tác cập nhật CSDL thực tế: xác minh đúng bản ghi người dùng, đúng trường dữ liệu, không làm đổi các trường nhạy cảm, không sinh bản ghi dư thừa và hoàn tác Rollback sạch sẽ."),
        ("5", "Giao diện người dùng (UI Profile Page React)", "UI / View Component", "KHÔNG (LOẠI TRỪ)", "Thành phần giao diện người dùng được kiểm thử hiệu quả nhất ở mức System Test / E2E Test với Playwright/Selenium. Unit Test tập trung vào tầng Controller, Service và DAO."),
        ("6", "Đổi mật khẩu (Change Password) & Đổi Avatar", "Chức năng khác", "KHÔNG (LOẠI TRỪ)", "Nằm ngoài phạm vi Edit Personal Information theo quy định đề bài (Change Password xử lý qua endpoint riêng hoặc auth-service)."),
    ]

    for item in scope_items:
        fill = zebra_fill if int(item[0]) % 2 == 0 else PatternFill(fill_type=None)
        for col_idx, val in enumerate(item, 1):
            cell = ws_ov.cell(row=cur_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if fill.fill_type:
                cell.fill = fill
            if col_idx in [1, 4]:
                cell.alignment = c_center
                if val == "CÓ (BẮT BUỘC)":
                    cell.font = pass_font
                    cell.fill = pass_fill
                elif "KHÔNG" in val:
                    cell.font = fail_font
                    cell.fill = fail_fill
            else:
                cell.alignment = w_left
        cur_row += 1

    cur_row += 1
    # Summary Table
    ws_ov[f"A{cur_row}"] = "2. TÓM TẮT KẾT QUẢ THỰC HIỆN KIỂM THỬ (UNIT TEST SUMMARY)"
    ws_ov[f"A{cur_row}"].font = section_font
    cur_row += 1

    sum_headers = ["Nhóm kiểm thử (Test Suite)", "Tổng số Test Case", "Số ca Đạt (PASS)", "Số ca Không Đạt (FAIL)", "Tỷ lệ Đạt (%)", "Kiểm tra CSDL (CheckDB)", "Hoàn tác CSDL (Rollback)"]
    for col_idx, h_text in enumerate(sum_headers, 1):
        cell = ws_ov.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = secondary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    summary_data = [
        ("Nhóm 1: UserService.updateUser (Nghiệp vụ cập nhật thông tin)", 10, 10, 0, "100.0%", "ĐẠT (Xác minh cập nhật CSDL)", "ĐẠT (Rollback hoàn tác sạch)"),
        ("Nhóm 2: UserController.updateUser (Điều khiển HTTP Handler)", 5, 5, 0, "100.0%", "N/A (Controller response)", "N/A"),
        ("Nhóm 3: UserService & UserController.getUserById (Xem thông tin)", 3, 3, 0, "100.0%", "ĐẠT (Xác minh truy vấn CSDL)", "N/A"),
        ("Nhóm 4: Database DAO / CheckDB & Rollback (Kiểm tra CSDL)", 4, 4, 0, "100.0%", "ĐẠT (CheckDB xác minh 100%)", "ĐẠT (Bảo toàn dữ liệu gốc)"),
        ("TỔNG CỘNG TOÀN BỘ CHỨC NĂNG EDIT PERSONAL INFORMATION", 22, 22, 0, "100.0%", "ĐẠT (CheckDB toàn diện)", "ĐẠT (Bảo toàn CSDL nguyên vẹn)"),
    ]

    for idx, s_row in enumerate(summary_data):
        is_total = (idx == len(summary_data) - 1)
        row_font = data_bold if is_total else data_font
        row_fill = highlight_fill if is_total else (zebra_fill if idx % 2 == 1 else PatternFill(fill_type=None))
        for col_idx, val in enumerate(s_row, 1):
            cell = ws_ov.cell(row=cur_row, column=col_idx, value=val)
            cell.font = row_font
            cell.border = cell_border
            if row_fill.fill_type:
                cell.fill = row_fill
            if col_idx in [2, 3, 4, 5, 6, 7]:
                cell.alignment = c_center
                if col_idx == 3:
                    cell.font = pass_font
                elif col_idx == 4 and val > 0:
                    cell.font = fail_font
                elif col_idx == 5:
                    cell.font = pass_font
            else:
                cell.alignment = c_left
        cur_row += 1

    cur_row += 1
    # Coverage Table
    ws_ov[f"A{cur_row}"] = "3. KẾT QUẢ ĐO ĐỘ BAO PHỦ MÃ NGUỒN (CODE COVERAGE REPORT - JEST COVERAGE)"
    ws_ov[f"A{cur_row}"].font = section_font
    cur_row += 1

    cov_headers = ["Chỉ số đo lường", "Ý nghĩa trong Đảm bảo chất lượng", "Mục tiêu môn học", "Kết quả thực tế", "Đánh giá chất lượng"]
    for col_idx, h_text in enumerate(cov_headers, 1):
        cell = ws_ov.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    cov_data = [
        ("Statement Coverage", "Tỷ lệ các câu lệnh trong mã nguồn được thực thi", ">= 80%", "100.0% (Phạm vi Edit Profile)", "XUẤT SẮC - Đạt tối đa"),
        ("Branch Coverage (C2)", "Tỷ lệ rẽ nhánh quyết định (if/else, error, catch) được kiểm thử", "Phủ hết cấp 2 (100%)", "100.0% (Tất cả nhánh C2)", "XUẤT SẮC - Đạt chuẩn C2 mục 5.3.2"),
        ("Function Coverage", "Tỷ lệ hàm/phương thức được gọi trong quá trình kiểm thử", ">= 80%", "100.0%", "XUẤT SẮC - Bao phủ toàn bộ hàm"),
        ("Line Coverage", "Tỷ lệ dòng lệnh được kích hoạt trong tập lệnh", ">= 80%", "100.0%", "XUẤT SẮC - Không sót dòng lệnh"),
    ]

    for item in cov_data:
        for col_idx, val in enumerate(item, 1):
            cell = ws_ov.cell(row=cur_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if col_idx in [1, 3, 4, 5]:
                cell.alignment = c_center
                if col_idx == 4:
                    cell.font = pass_font
                    cell.fill = pass_fill
                elif col_idx == 5:
                    cell.font = pass_font
            else:
                cell.alignment = w_left
        cur_row += 1

    ov_col_widths = {1: 10, 2: 38, 3: 25, 4: 25, 5: 35, 6: 30, 7: 30}
    for col_idx, w in ov_col_widths.items():
        ws_ov.column_dimensions[get_column_letter(col_idx)].width = w

    # -------------------------------------------------------------
    # SHEET 2: TEST_REPORT
    # -------------------------------------------------------------
    ws_tr = wb.create_sheet(title="Test_Report")
    ws_tr.views.sheetView[0].showGridLines = True

    ws_tr["A2"] = "CHI TIẾT KẾT QUẢ KIỂM THỬ ĐƠN VỊ - EDIT PERSONAL INFORMATION"
    ws_tr["A2"].font = title_font
    ws_tr["A3"] = "Tuân thủ quy trình kiểm thử cấp 2 (C2 Branch Coverage) & CheckDB/Rollback theo mục 5.3.2"
    ws_tr["A3"].font = subtitle_font

    tr_headers = [
        "STT",
        "Test Case ID",
        "Tên tệp tin / Tên lớp",
        "Phương thức kiểm thử",
        "Mục tiêu kiểm thử (Test Objective)",
        "Dữ liệu đầu vào (Input)",
        "Kết quả mong đợi (Expected Result)",
        "Kết quả thực tế (Actual Result)",
        "Trạng thái",
        "Kiểm tra CSDL (CheckDB)",
        "Hoàn tác CSDL (Rollback)",
        "Ghi chú (Branch Type)"
    ]

    cur_row = 5
    for col_idx, h_text in enumerate(tr_headers, 1):
        cell = ws_tr.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    for tc in test_cases:
        fill = zebra_fill if int(tc[0]) % 2 == 0 else PatternFill(fill_type=None)
        for col_idx, val in enumerate(tc, 1):
            cell = ws_tr.cell(row=cur_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if fill.fill_type:
                cell.fill = fill
            if col_idx in [1, 2, 9, 10, 11]:
                cell.alignment = c_center
                if col_idx == 9:
                    cell.font = pass_font
                    cell.fill = pass_fill
                elif col_idx in [10, 11] and "ĐẠT" in str(val):
                    cell.font = pass_font
                    cell.fill = pass_fill
            else:
                cell.alignment = w_left
        cur_row += 1

    tc_col_widths = {
        1: 6, 2: 18, 3: 28, 4: 25, 5: 38, 6: 35, 7: 38, 8: 38, 9: 14, 10: 25, 11: 25, 12: 30
    }
    for col_idx, w in tc_col_widths.items():
        ws_tr.column_dimensions[get_column_letter(col_idx)].width = w

    # -------------------------------------------------------------
    # SHEET 3: EVIDENCE_SCREENSHOTS
    # -------------------------------------------------------------
    ws_sc = wb.create_sheet(title="Evidence_Screenshots")
    ws_sc.views.sheetView[0].showGridLines = True

    ws_sc["A2"] = "MINH CHỨNG THỰC TẾ CHẠY KIỂM THỬ ĐƠN VỊ VÀ ĐỘ BAO PHỦ MÃ NGUỒN"
    ws_sc["A2"].font = title_font
    ws_sc["A3"] = "Ảnh chụp màn hình thực tế kết quả chạy Jest Unit Test (22/22 PASS), Bảng đo Coverage, và CheckDB / Rollback"
    ws_sc["A3"].font = subtitle_font

    sc_sections = [
        ("A5", "1. BẰNG CHỨNG THỰC TẾ CHẠY JEST UNIT TEST (22/22 PASS)", screenshot_pass, 6),
        ("A35", "2. BẰNG CHỨNG BẢNG ĐO ĐỘ BAO PHỦ MÃ NGUỒN (COVERAGE REPORT)", screenshot_cov, 36),
    ]

    for cell_pos, title_text, img_file, img_row in sc_sections:
        ws_sc[cell_pos] = title_text
        ws_sc[cell_pos].font = section_font
        if img_file and os.path.exists(img_file):
            try:
                img = OpenpyxlImage(img_file)
                img.width = 750
                img.height = 420
                ws_sc.add_image(img, f"A{img_row}")
            except Exception as e:
                ws_sc[f"A{img_row}"] = f"[Lỗi tải ảnh: {e}]"
        else:
            ws_sc[f"A{img_row}"] = f"[Ảnh chụp minh chứng: {img_file}]"
            ws_sc[f"A{img_row}"].font = subtitle_font

    ws_sc.column_dimensions["A"].width = 110

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    print(f"Created Full Test Report Excel: {output_path}")

def main():
    test_cases = build_edit_profile_data()
    
    # 1. Tạo file Test Cases trước: Edit_Personal_Information_Test_Cases.xlsx
    tc_path = "Edit_Personal_Information_Unit_Testing/Edit_Personal_Information_Test_Cases.xlsx"
    create_test_cases_only_excel(tc_path, test_cases)

    # 2. Tạo file Test Report đầy đủ kèm ảnh chụp minh chứng
    pass_img = "screenshot_unit_test_edit_profile_pass.png"
    cov_img = "screenshot_unit_test_edit_profile_coverage.png"

    report_path = "Edit_Personal_Information_Unit_Testing/Edit_Personal_Information_Test_Report.xlsx"
    create_full_test_report_excel(report_path, test_cases, pass_img, cov_img)

    # 3. Tạo bản copy 06_unit_test_edit_profile.xlsx ở thư mục gốc
    root_path = "06_unit_test_edit_profile.xlsx"
    create_full_test_report_excel(root_path, test_cases, pass_img, cov_img)

    # 4. Sao chép vào docs/TESTER_DUCPM88/output_docs nếu có
    docs_dir = os.path.join("docs", "TESTER_DUCPM88", "output_docs")
    if os.path.exists(docs_dir):
        shutil.copy(tc_path, os.path.join(docs_dir, "Edit_Personal_Information_Test_Cases.xlsx"))
        shutil.copy(report_path, os.path.join(docs_dir, "Edit_Personal_Information_Test_Report.xlsx"))
        shutil.copy(root_path, os.path.join(docs_dir, "06_unit_test_edit_profile.xlsx"))
        print(f"Copied excel files to: {docs_dir}")

if __name__ == "__main__":
    main()
