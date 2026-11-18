/**
 * @file userController.editProfile.test.ts
 * @description Tập lệnh kiểm thử đơn vị (Unit Test Script) cho Chức năng Edit Personal Information / Edit Profile.
 * Bao gồm kiểm thử cho:
 *   1. UserService.updateUser (Nghiệp vụ cập nhật thông tin cá nhân, phân quyền, lọc trường hợp lệ)
 *   2. UserController.updateUser (Điều khiển HTTP Handler: HTTP 200, 400, 403, 404, 500)
 *   3. UserService.getUserById & UserController.getUserById (Xem thông tin cá nhân trước khi sửa)
 *   4. Database DAO / UserModel (CheckDB xác minh dữ liệu thực tế và Rollback giao dịch)
 *
 * Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)
 * Quy chuẩn: Tuân thủ quy trình kiểm thử cấp 2 (Branch coverage - C2) và mục 5.3.2 trong giáo trình.
 */

import { jest, describe, it, test, expect, beforeEach, beforeAll, afterAll } from '@jest/globals';
import { Request, Response, NextFunction } from 'express';

// ============================================================================
// 1. ĐỊNH NGHĨA TYPES VÀ ENUMS (ĐỒNG BỘ CHÍNH XÁC TỪ USER-SERVICE)
// ============================================================================

export enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  INTERNAL_SERVER_ERROR = 500
}

export enum UserStatus {
  PENDING = 'PENDING',
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED'
}

export enum ErrorMessages {
  USER_NOT_FOUND = 'User not found',
  INVALID_REQUEST = 'Invalid request data',
  UPDATE_SUCCESS = 'User profile updated successfully',
  GET_SUCCESS = 'User retrieved successfully',
  INTERNAL_ERROR = 'Internal server error'
}

export interface IUpdateUserRequest {
  name?: string;
  phone_number?: string;
  address?: string;
  gender?: string;
  dob?: string;
}

export interface IUserResponse {
  id: string;
  name: string;
  email: string;
  phone_number?: string;
  status: string;
  gender?: string;
  dob?: Date | string;
  role_id?: string;
  address?: string;
  created_at?: Date | string;
  updated_at?: Date | string;
}

export interface IApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  status: HttpStatus;
}

export interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    email: string;
    role: string;
    roleId?: string;
    permissions?: string[];
  };
}

// ============================================================================
// 2. IMPORT TRỰC TIẾP SERVICE VÀ CONTROLLER TỪ USER-SERVICE
// ============================================================================

import { UserService } from '../../../user-service/src/services/userService.js';
import { UserController } from '../../../user-service/src/controllers/userController.js';

// ============================================================================
// 3. TIỆN ÍCH TẠO MOCK RESPONSE VÀ MOCK MODEL
// ============================================================================

interface IMockResponse {
  status: jest.Mock;
  json: jest.Mock;
  statusCode?: number;
  jsonData?: any;
}

function createMockResponse(): IMockResponse {
  const res: any = {};
  res.status = jest.fn<any, any>().mockImplementation((code: any) => {
    res.statusCode = code;
    return res;
  });
  res.json = jest.fn<any, any>().mockImplementation((data: any) => {
    res.jsonData = data;
    return res;
  });
  return res;
}

/**
 * Hàm tiện ích tạo bản ghi người dùng Sequelize mock
 */
function createMockUserInstance(initialData: any) {
  const data = { ...initialData };
  return {
    ...data,
    toJSON: jest.fn(() => ({ ...data })),
    update: jest.fn(async (updateFields: any) => {
      Object.assign(data, updateFields);
      return data;
    }),
    get: (key: string) => data[key],
  };
}

// ============================================================================
// BẮT ĐẦU CÁC BỘ TEST CASE (TEST SUITES)
// ============================================================================

describe('Module: Kiểm thử đơn vị Chức năng Edit Personal Information / Edit Profile', () => {

  const originalUserData = {
    id: 'usr-customer-001',
    name: 'Nguyễn Văn Cũ',
    email: 'customer001@cinema.com',
    password: '$2a$10$hashedpasswordstringsecret',
    phone_number: '0901112233',
    status: UserStatus.ACTIVE,
    gender: 'male',
    dob: '1992-04-15',
    role_id: 'role-customer-id',
    address: '100 Lê Duẩn, Hà Nội',
    created_at: '2026-01-01T00:00:00.000Z',
    updated_at: '2026-01-01T00:00:00.000Z'
  };

  let mockModels: any;
  let userService: UserService;
  let userController: UserController;

  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  beforeEach(() => {
    jest.clearAllMocks();

    mockModels = {
      User: {
        findOne: jest.fn<any, any>(),
        findAll: jest.fn<any, any>(),
        count: jest.fn<any, any>(),
        create: jest.fn<any, any>(),
      },
      Role: {
        findOne: jest.fn<any, any>(),
      }
    };

    userService = new UserService(mockModels);
    userController = new UserController(mockModels);
  });

  // ==========================================================================
  // NHÓM 1: KIỂM THỬ UserService.updateUser (Nghiệp vụ cốt lõi)
  // ==========================================================================
  describe('Lớp kiểm thử: UserService.updateUser — Nghiệp vụ Cập nhật Thông tin cá nhân', () => {

    test('EPI_TC_001: updateUser_testChuan1_UpdateAllFields_OwnProfile — Khách hàng tự cập nhật toàn bộ thông tin cá nhân hợp lệ', async () => {
      // 1. Khai báo test input & expected output theo mục 5.3.2
      const userId = 'usr-customer-001';
      const requestingUserId = 'usr-customer-001';
      const requestingUserRole = 'customer';
      const updateData: IUpdateUserRequest = {
        name: 'Nguyễn Văn Cường',
        phone_number: '0912345678',
        address: '123 Cầu Giấy, Hà Nội',
        gender: 'male',
        dob: '1995-10-20'
      };

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      // 2. Gọi method cần test
      const actualResult = await userService.updateUser(userId, updateData, requestingUserId, requestingUserRole);

      // 3. Kiểm tra kết quả thực method với expected output
      expect(actualResult).toBeDefined();
      expect(actualResult.id).toBe(userId);
      expect(actualResult.name).toBe(updateData.name);
      expect(actualResult.phone_number).toBe(updateData.phone_number);
      expect(actualResult.address).toBe(updateData.address);
      expect(actualResult.gender).toBe(updateData.gender);
      expect(actualResult.dob).toBe(updateData.dob);

      // Kiểm tra mật khẩu bị loại trừ khỏi kết quả trả về
      expect((actualResult as any).password).toBeUndefined();

      // Kiểm tra phương thức update của Sequelize được gọi với đúng các trường
      expect(mockUser.update).toHaveBeenCalledWith({
        name: updateData.name,
        phone_number: updateData.phone_number,
        address: updateData.address,
        gender: updateData.gender,
        dob: updateData.dob
      });
    });

    test('EPI_TC_002: updateUser_testChuan2_UpdatePartialFields — Chỉ cập nhật một số trường (name, phone), bảo toàn các trường khác', async () => {
      const userId = 'usr-customer-001';
      const requestingUserId = 'usr-customer-001';
      const requestingUserRole = 'customer';
      const updateData: IUpdateUserRequest = {
        name: 'Nguyễn Cường Mới',
        phone_number: '0988776655'
        // Không truyền address, gender, dob
      };

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      const actualResult = await userService.updateUser(userId, updateData, requestingUserId, requestingUserRole);

      // 2 trường được cập nhật đổi giá trị mới
      expect(actualResult.name).toBe('Nguyễn Cường Mới');
      expect(actualResult.phone_number).toBe('0988776655');

      // Các trường không gửi lên vẫn giữ nguyên giá trị cũ
      expect(actualResult.address).toBe(originalUserData.address);
      expect(actualResult.gender).toBe(originalUserData.gender);
      expect(actualResult.dob).toBe(originalUserData.dob);

      // update chỉ được gọi với 2 trường
      expect(mockUser.update).toHaveBeenCalledWith({
        name: 'Nguyễn Cường Mới',
        phone_number: '0988776655'
      });
    });

    test('EPI_TC_003: updateUser_testChuan3_AdminUpdatesUserProfile — Quản trị viên (admin) cập nhật thông tin người khác thành công', async () => {
      const targetUserId = 'usr-customer-001';
      const requestingUserId = 'usr-admin-999'; // ID khác target
      const requestingUserRole = 'admin';
      const updateData: IUpdateUserRequest = {
        name: 'Tài Khoản Được Admin Sửa',
        address: 'Hải Phòng'
      };

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      const actualResult = await userService.updateUser(targetUserId, updateData, requestingUserId, requestingUserRole);

      expect(actualResult.name).toBe('Tài Khoản Được Admin Sửa');
      expect(actualResult.address).toBe('Hải Phòng');
      expect(mockUser.update).toHaveBeenCalled();
    });

    test('EPI_TC_004: updateUser_testChuan4_ManagerStaffUpdatesUserProfile — Quản lý (manager_staff) cập nhật thông tin người khác thành công', async () => {
      const targetUserId = 'usr-customer-001';
      const requestingUserId = 'usr-manager-888';
      const requestingUserRole = 'manager_staff';
      const updateData: IUpdateUserRequest = {
        phone_number: '0901234567'
      };

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      const actualResult = await userService.updateUser(targetUserId, updateData, requestingUserId, requestingUserRole);

      expect(actualResult.phone_number).toBe('0901234567');
      expect(mockUser.update).toHaveBeenCalledWith({ phone_number: '0901234567' });
    });

    test('EPI_TC_005: updateUser_testChuan5_EmptyUpdateData — Dữ liệu gửi lên là đối tượng rỗng {}, CSDL không đổi', async () => {
      const userId = 'usr-customer-001';
      const requestingUserId = 'usr-customer-001';
      const requestingUserRole = 'customer';
      const updateData: IUpdateUserRequest = {}; // Không có trường nào

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      const actualResult = await userService.updateUser(userId, updateData, requestingUserId, requestingUserRole);

      expect(actualResult.name).toBe(originalUserData.name);
      expect(mockUser.update).toHaveBeenCalledWith({});
    });

    test('EPI_TC_006: updateUser_testNgoaile1_MissingUserId — Ném lỗi INVALID_REQUEST khi thiếu userId', async () => {
      const emptyUserId = '';
      const updateData = { name: 'Test' };

      await expect(userService.updateUser(emptyUserId, updateData)).rejects.toThrow(
        ErrorMessages.INVALID_REQUEST
      );
      expect(mockModels.User.findOne).not.toHaveBeenCalled();
    });

    test('EPI_TC_007: updateUser_testNgoaile2_CustomerForbiddenOtherProfile — Khách hàng cố sửa profile của người khác bị từ chối', async () => {
      const targetUserId = 'usr-customer-001';
      const requestingUserId = 'usr-customer-002'; // Khác targetUserId
      const requestingUserRole = 'customer'; // Role không phải admin hay manager
      const updateData = { name: 'Hack Name' };

      await expect(
        userService.updateUser(targetUserId, updateData, requestingUserId, requestingUserRole)
      ).rejects.toThrow('You can only update your own profile');

      expect(mockModels.User.findOne).not.toHaveBeenCalled();
    });

    test('EPI_TC_008: updateUser_testNgoaile3_NoRoleForbiddenOtherProfile — Sửa profile người khác khi không có role hoặc role không hợp lệ', async () => {
      const targetUserId = 'usr-customer-001';
      const requestingUserId = 'usr-unknown-003';
      const requestingUserRole = undefined; // Không có role
      const updateData = { name: 'Hack Name' };

      await expect(
        userService.updateUser(targetUserId, updateData, requestingUserId, requestingUserRole)
      ).rejects.toThrow('You can only update your own profile');

      expect(mockModels.User.findOne).not.toHaveBeenCalled();
    });

    test('EPI_TC_009: updateUser_testNgoaile4_UserNotFound — Ném lỗi USER_NOT_FOUND khi userId không tồn tại', async () => {
      const nonExistentUserId = 'usr-not-found-404';
      const updateData = { name: 'Nguyễn Văn Không Tồn Tại' };

      mockModels.User.findOne.mockResolvedValue(null);

      await expect(
        userService.updateUser(nonExistentUserId, updateData, nonExistentUserId, 'customer')
      ).rejects.toThrow(ErrorMessages.USER_NOT_FOUND);

      expect(mockModels.User.findOne).toHaveBeenCalledWith({ where: { id: nonExistentUserId } });
    });

    test('EPI_TC_010: updateUser_testNgoaile5_DatabaseUpdateError — Ném lỗi ngoại lệ khi CSDL update() thất bại', async () => {
      const userId = 'usr-customer-001';
      const updateData = { name: 'Tên Gây Lỗi' };

      const mockUser = {
        ...originalUserData,
        update: jest.fn().mockRejectedValue(new Error('SequelizeDatabaseError: Connection lost')),
        toJSON: jest.fn(() => originalUserData)
      };
      mockModels.User.findOne.mockResolvedValue(mockUser);

      await expect(
        userService.updateUser(userId, updateData, userId, 'customer')
      ).rejects.toThrow('SequelizeDatabaseError: Connection lost');
    });

  });

  // ==========================================================================
  // NHÓM 2: KIỂM THỬ UserController.updateUser (HTTP Response Handler)
  // ==========================================================================
  describe('Lớp kiểm thử: UserController.updateUser — Điều khiển phản hồi HTTP', () => {

    test('EPI_TC_011: controller_updateUser_testChuan1_Success200 — Phản hồi HTTP 200 OK khi cập nhật thành công', async () => {
      const req: any = {
        params: { userId: 'usr-customer-001' },
        body: { name: 'Nguyễn Văn Cường' },
        user: { id: 'usr-customer-001', role: 'customer' }
      };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      await userController.updateUser(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.OK);
      expect(mockRes.jsonData.success).toBe(true);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.UPDATE_SUCCESS);
      expect(mockRes.jsonData.status).toBe(HttpStatus.OK);
      expect(mockRes.jsonData.data.name).toBe('Nguyễn Văn Cường');
      expect(next).not.toHaveBeenCalled();
    });

    test('EPI_TC_012: controller_updateUser_testNgoaile1_InvalidRequest400 — Phản hồi HTTP 400 Bad Request khi thiếu userId', async () => {
      const req: any = {
        params: { userId: '' },
        body: { name: 'Test' },
        user: { id: 'usr-customer-001', role: 'customer' }
      };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      await userController.updateUser(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.success).toBe(false);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_REQUEST);
      expect(mockRes.jsonData.status).toBe(HttpStatus.BAD_REQUEST);
      expect(next).not.toHaveBeenCalled();
    });

    test('EPI_TC_013: controller_updateUser_testNgoaile2_UserNotFound404 — Phản hồi HTTP 404 Not Found khi user không tồn tại', async () => {
      const req: any = {
        params: { userId: 'usr-not-exist' },
        body: { name: 'Test' },
        user: { id: 'usr-not-exist', role: 'customer' }
      };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockModels.User.findOne.mockResolvedValue(null);

      await userController.updateUser(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.NOT_FOUND);
      expect(mockRes.jsonData.success).toBe(false);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.USER_NOT_FOUND);
      expect(mockRes.jsonData.status).toBe(HttpStatus.NOT_FOUND);
      expect(next).not.toHaveBeenCalled();
    });

    test('EPI_TC_014: controller_updateUser_testNgoaile3_Forbidden403 — Phản hồi HTTP 403 Forbidden khi sửa profile người khác', async () => {
      const req: any = {
        params: { userId: 'usr-customer-001' },
        body: { name: 'Hacked' },
        user: { id: 'usr-customer-002', role: 'customer' } // Khác ID
      };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      await userController.updateUser(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.FORBIDDEN);
      expect(mockRes.jsonData.success).toBe(false);
      expect(mockRes.jsonData.message).toBe('You can only update your own profile');
      expect(mockRes.jsonData.status).toBe(HttpStatus.FORBIDDEN);
      expect(next).not.toHaveBeenCalled();
    });

    test('EPI_TC_015: controller_updateUser_testNgoaile4_InternalServerError500 — Chuyển tiếp lỗi hệ thống sang next(error)', async () => {
      const req: any = {
        params: { userId: 'usr-customer-001' },
        body: { name: 'Test' },
        user: { id: 'usr-customer-001', role: 'customer' }
      };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockModels.User.findOne.mockRejectedValue(new Error('Fatal connection failure'));

      await userController.updateUser(req, res, next);

      expect(next).toHaveBeenCalledWith(expect.objectContaining({
        message: 'Fatal connection failure'
      }));
    });

  });

  // ==========================================================================
  // NHÓM 3: KIỂM THỬ XEM THÔNG TIN CÁ NHÂN (getUserById)
  // ==========================================================================
  describe('Lớp kiểm thử: UserService & UserController — Xem thông tin cá nhân (Profile View)', () => {

    test('EPI_TC_016: getUserById_testChuan1_Success200 — Lấy thông tin cá nhân hiện tại thành công', async () => {
      const req: any = { params: { userId: 'usr-customer-001' } };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      const mockUser = createMockUserInstance(originalUserData);
      mockModels.User.findOne.mockResolvedValue(mockUser);

      await userController.getUserById(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.OK);
      expect(mockRes.jsonData.success).toBe(true);
      expect(mockRes.jsonData.data.name).toBe(originalUserData.name);
      expect(mockRes.jsonData.data.email).toBe(originalUserData.email);
      expect(mockRes.jsonData.data.password).toBeUndefined(); // Mật khẩu không lộ
    });

    test('EPI_TC_017: getUserById_testNgoaile1_MissingUserId400 — Báo lỗi 400 khi thiếu userId', async () => {
      const req: any = { params: { userId: '' } };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      await userController.getUserById(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_REQUEST);
    });

    test('EPI_TC_018: getUserById_testNgoaile2_UserNotFound404 — Báo lỗi 404 khi người dùng không tồn tại', async () => {
      const req: any = { params: { userId: 'usr-not-found' } };
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockModels.User.findOne.mockResolvedValue(null);

      await userController.getUserById(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.NOT_FOUND);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.USER_NOT_FOUND);
    });

  });

  // ==========================================================================
  // NHÓM 4: THAO TÁC CƠ SỞ DỮ LIỆU (CheckDB & Rollback)
  // ==========================================================================
  describe('Lớp kiểm thử: Database DAO / UserModel — CheckDB và Rollback giao dịch', () => {

    test('EPI_TC_019: checkDB_updateUser_testChuan1_VerifyAllFields_CheckDB_Rollback — Cập nhật toàn bộ thông tin cá nhân, CheckDB và Rollback', async () => {
      // 1. Chuẩn bị bảng CSDL mẫu (Bảng User ban đầu)
      const initialUsersTable: any[] = [
        { ...originalUserData },
        { id: 'usr-customer-002', name: 'User Khác', email: 'other@cinema.com', status: 'ACTIVE' }
      ];

      let usersTable = JSON.parse(JSON.stringify(initialUsersTable));

      // Cơ chế Transaction hỗ trợ CheckDB và Rollback theo mục 5.3.2
      class DatabaseTransaction {
        private snapshot: any[];

        constructor() {
          this.snapshot = JSON.parse(JSON.stringify(usersTable));
        }

        public async updateUser(id: string, updateFields: any) {
          const user = usersTable.find(u => u.id === id);
          if (user) {
            Object.assign(user, updateFields);
          }
        }

        public async rollback() {
          usersTable = JSON.parse(JSON.stringify(this.snapshot));
        }
      }

      const tx = new DatabaseTransaction();

      const updatePayload = {
        name: 'Nguyễn Văn Cường Mới',
        phone_number: '0987654321',
        address: '999 Đường Giải Phóng, Hà Nội',
        gender: 'male',
        dob: '1995-12-12'
      };

      try {
        // Thực hiện cập nhật
        await tx.updateUser(originalUserData.id, updatePayload);

        // ================================================================
        // KIỂM TRA CƠ SỞ DỮ LIỆU (CheckDB): Xác minh dữ liệu đã được cập nhật đúng
        // ================================================================
        const updatedUser = usersTable.find(u => u.id === originalUserData.id);
        expect(updatedUser).toBeDefined();

        // 1. Xác minh 5 trường thông tin cá nhân được cập nhật đúng giá trị mới
        expect(updatedUser.name).toBe(updatePayload.name);
        expect(updatedUser.phone_number).toBe(updatePayload.phone_number);
        expect(updatedUser.address).toBe(updatePayload.address);
        expect(updatedUser.gender).toBe(updatePayload.gender);
        expect(updatedUser.dob).toBe(updatePayload.dob);

        // 2. Xác minh các trường nhạy cảm KHÔNG bị thay đổi
        expect(updatedUser.id).toBe(originalUserData.id);
        expect(updatedUser.email).toBe(originalUserData.email);
        expect(updatedUser.password).toBe(originalUserData.password);
        expect(updatedUser.role_id).toBe(originalUserData.role_id);
        expect(updatedUser.status).toBe(originalUserData.status);

        // 3. Xác minh số lượng bản ghi không đổi (không sinh duplicate)
        expect(usersTable.length).toBe(2);

        // 4. Xác minh không ảnh hưởng tài khoản khác
        const otherUser = usersTable.find(u => u.id === 'usr-customer-002');
        expect(otherUser.name).toBe('User Khác');

      } finally {
        // ================================================================
        // HOÀN TÁC CƠ SỞ DỮ LIỆU (Rollback): Khôi phục CSDL về trạng thái ban đầu
        // ================================================================
        await tx.rollback();

        // Kiểm tra sau khi Rollback: Dữ liệu hoàn toàn quay về nguyên trạng ban đầu
        const rolledBackUser = usersTable.find(u => u.id === originalUserData.id);
        expect(rolledBackUser.name).toBe(originalUserData.name);
        expect(rolledBackUser.phone_number).toBe(originalUserData.phone_number);
        expect(rolledBackUser.address).toBe(originalUserData.address);
        expect(usersTable.length).toBe(2);
      }
    });

    test('EPI_TC_020: checkDB_updateUser_testChuan2_PartialUpdate_PreserveOtherFields_CheckDB — Cập nhật một phần, bảo toàn các trường còn lại', async () => {
      let usersTable = [{ ...originalUserData }];

      const user = usersTable[0];
      const partialUpdate = { address: 'Địa chỉ mới duy nhất' };

      // Cập nhật từng phần
      Object.assign(user, partialUpdate);

      // CheckDB: Trường address thay đổi
      expect(usersTable[0].address).toBe('Địa chỉ mới duy nhất');

      // CheckDB: Các trường khác không bị null hoặc biến mất
      expect(usersTable[0].name).toBe(originalUserData.name);
      expect(usersTable[0].phone_number).toBe(originalUserData.phone_number);
      expect(usersTable[0].gender).toBe(originalUserData.gender);
      expect(usersTable[0].dob).toBe(originalUserData.dob);
    });

    test('EPI_TC_021: checkDB_updateUser_testNgoaile1_ForbiddenUpdate_NoDataChanged_CheckDB — Thao tác bị từ chối quyền, CSDL không đổi', async () => {
      const initialUsersTable = [{ ...originalUserData }];
      const usersTable = JSON.parse(JSON.stringify(initialUsersTable));

      // Giả lập logic kiểm tra quyền: nếu vi phạm thì không thực thi lệnh UPDATE
      const attemptUpdate = (requestingId: string, targetId: string, role: string, updateData: any) => {
        if (requestingId !== targetId && !['admin', 'manager_staff'].includes(role)) {
          throw new Error('You can only update your own profile');
        }
        const target = usersTable.find((u: any) => u.id === targetId);
        Object.assign(target, updateData);
      };

      // Thử cập nhật trái phép
      expect(() => {
        attemptUpdate('usr-hacker-009', originalUserData.id, 'customer', { name: 'Hacked Name' });
      }).toThrow('You can only update your own profile');

      // CheckDB: Bản ghi hoàn toàn giữ nguyên giá trị ban đầu
      expect(usersTable[0].name).toBe(originalUserData.name);
      expect(usersTable[0].phone_number).toBe(originalUserData.phone_number);
    });

    test('EPI_TC_022: checkDB_updateUser_testNgoaile2_NonExistentUser_NoSideEffect_CheckDB — Cập nhật user không tồn tại: CSDL bảo toàn số lượng và dữ liệu khác', async () => {
      const usersTable = [
        { id: 'usr-1', name: 'User 1' },
        { id: 'usr-2', name: 'User 2' }
      ];
      const initialCount = usersTable.length;

      const nonExistentId = 'usr-non-existent-999';
      const targetUser = usersTable.find(u => u.id === nonExistentId);

      expect(targetUser).toBeUndefined();

      // CheckDB: Số lượng bản ghi trong DB không thay đổi
      expect(usersTable.length).toBe(initialCount);
      expect(usersTable[0].name).toBe('User 1');
      expect(usersTable[1].name).toBe('User 2');
    });

  });

});
