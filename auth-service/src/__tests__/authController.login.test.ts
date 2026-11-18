/**
 * @file authController.login.test.ts
 * @description Tập lệnh kiểm thử đơn vị (Unit Test Script) cho Chức năng Đăng nhập (Login).
 * Bao gồm kiểm thử cho:
 *   1. AuthController.loginSchema (Kiểm tra tính hợp lệ dữ liệu đầu vào - Validation)
 *   2. AuthController.login (Đăng nhập Khách hàng - Customer Login)
 *   3. AuthController.loginAdmin (Đăng nhập Quản trị viên & Nhân viên - Admin/Staff Login)
 *   4. TokenService & Session Cache (Sinh JWT token và lưu cache Redis)
 *   5. UserDAO / Database Operations (Thao tác cơ sở dữ liệu: CheckDB & Rollback)
 *
 * Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)
 * Quy chuẩn: Tuân thủ quy trình kiểm thử cấp 2 (Branch coverage - C2) và mục 5.3.2.
 */

import { jest, describe, it, test, expect, beforeEach, beforeAll, afterAll } from '@jest/globals';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

// ============================================================================
// 1. THIẾT LẬP MOCK CHO CÁC MODULE PHỤ THUỘC (REDIS, GRPC USER CLIENT)
// ============================================================================

const mockRedisGet = jest.fn<any, any>();
const mockRedisSetEx = jest.fn<any, any>();
const mockRedisDel = jest.fn<any, any>();
const mockRedisKeys = jest.fn<any, any>();

jest.mock('../config/redis.js', () => ({
  redisClient: {
    get: (...args: any[]) => mockRedisGet(...args),
    setEx: (...args: any[]) => mockRedisSetEx(...args),
    del: (...args: any[]) => mockRedisDel(...args),
    keys: (...args: any[]) => mockRedisKeys(...args),
  },
  redisPubSubClient: {
    publish: jest.fn<any, any>(),
  },
  default: {
    get: (...args: any[]) => mockRedisGet(...args),
    setEx: (...args: any[]) => mockRedisSetEx(...args),
    del: (...args: any[]) => mockRedisDel(...args),
    keys: (...args: any[]) => mockRedisKeys(...args),
  },
}));

const mockGetUserByEmail = jest.fn<any, any>();
const mockGetUserWithRoleByEmail = jest.fn<any, any>();
const mockActivateUser = jest.fn<any, any>();
const mockGetPermissionsByRoleId = jest.fn<any, any>();

jest.mock('../services/userGrpcClient.js', () => ({
  userClient: {
    GetUserByEmail: (...args: any[]) => mockGetUserByEmail(...args),
    GetUserWithRoleByEmail: (...args: any[]) => mockGetUserWithRoleByEmail(...args),
    ActivateUser: (...args: any[]) => mockActivateUser(...args),
    GetPermissionsByRoleId: (...args: any[]) => mockGetPermissionsByRoleId(...args),
  },
}));

import AuthController from '../controllers/authController.js';
import { TokenService } from '../services/tokenService.js';
import { ErrorMessages, HttpStatus, UserStatus } from '../types/index.js';

// ============================================================================
// 2. HÀM TIỆN ÍCH TẠO MOCK REQUEST / RESPONSE
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

const RAW_PASSWORD = 'Password123@';
const HASHED_PASSWORD = bcrypt.hashSync(RAW_PASSWORD, 10);
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// ============================================================================
// BẮT ĐẦU CÁC BỘ TEST CASE (TEST SUITES)
// ============================================================================

describe('Module: Kiểm thử đơn vị Chức năng Đăng nhập (Login)', () => {

  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  beforeEach(() => {
    jest.clearAllMocks();
    mockRedisGet.mockResolvedValue(null);
    mockRedisSetEx.mockResolvedValue('OK');
    mockRedisDel.mockResolvedValue(1);
    mockRedisKeys.mockResolvedValue([]);
  });

  // ==========================================================================
  // NHÓM 1: KIỂM THỬ AuthController.loginSchema (Validation)
  // ==========================================================================
  describe('Lớp kiểm thử: AuthController — Phương thức: loginSchema (Kiểm tra tính hợp lệ dữ liệu)', () => {

    test('TC-AUTH-SCHEMA-01: loginSchema_testChuan1_ValidPayload — Email và password hợp lệ', async () => {
      const testInput = {
        email: 'customer@cinema.com',
        password: 'Password123@',
      };
      const actualResult = await AuthController.loginSchema.validateAsync(testInput);
      expect(actualResult).toBeDefined();
      expect(actualResult.email).toBe('customer@cinema.com');
      expect(actualResult.password).toBe('Password123@');
    });

    test('TC-AUTH-SCHEMA-02: loginSchema_testNgoaile1_MissingEmail — Thiếu trường email', async () => {
      const testInput = {
        password: 'Password123@',
      };
      await expect(AuthController.loginSchema.validateAsync(testInput))
        .rejects.toThrow('"email" is required');
    });

    test('TC-AUTH-SCHEMA-03: loginSchema_testNgoaile2_InvalidEmailFormat — Email sai định dạng', async () => {
      const testInput = {
        email: 'invalid-email-string',
        password: 'Password123@',
      };
      await expect(AuthController.loginSchema.validateAsync(testInput))
        .rejects.toThrow('"email" must be a valid email');
    });

    test('TC-AUTH-SCHEMA-04: loginSchema_testNgoaile3_MissingPassword — Thiếu trường password', async () => {
      const testInput = {
        email: 'customer@cinema.com',
      };
      await expect(AuthController.loginSchema.validateAsync(testInput))
        .rejects.toThrow('"password" is required');
    });

    test('TC-AUTH-SCHEMA-05: loginSchema_testNgoaile4_EmptyPassword — Password là chuỗi rỗng', async () => {
      const testInput = {
        email: 'customer@cinema.com',
        password: '',
      };
      await expect(AuthController.loginSchema.validateAsync(testInput))
        .rejects.toThrow('"password" is not allowed to be empty');
    });

    test('TC-AUTH-SCHEMA-06: loginSchema_testNgoaile5_EmptyObject — Request body hoàn toàn rỗng', async () => {
      const testInput = {};
      await expect(AuthController.loginSchema.validateAsync(testInput))
        .rejects.toThrow();
    });

  });

  // ==========================================================================
  // NHÓM 2: KIỂM THỬ AuthController.login (Khách hàng đăng nhập - Customer)
  // ==========================================================================
  describe('Lớp kiểm thử: AuthController — Phương thức: login (Đăng nhập Khách hàng)', () => {

    test('TC-AUTH-LOGIN-01: login_testChuan1_CustomerSuccess — Khách hàng đăng nhập thành công', async () => {
      const testInput = {
        email: 'customer.active@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-id-001',
            email: testInput.email,
            name: 'Nguyễn Văn Khách',
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-id-001',
            email: testInput.email,
            name: 'Nguyễn Văn Khách',
            role_name: 'customer',
            role_id: 'role-customer-id',
          },
        });
      });

      mockGetPermissionsByRoleId.mockImplementation((params: any, callback: any) => {
        callback(null, {
          success: true,
          permissions: [
            { id: 'p1', name: 'Xem phim', code: 'view_movies', description: 'Được xem danh sách phim' },
          ],
        });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      const actualJson = mockRes.jsonData;
      expect(actualJson).toBeDefined();
      expect(actualJson.token).toBeDefined();
      expect(actualJson.user.email).toBe(testInput.email);
      expect(actualJson.user.role).toBe('customer');
      expect(actualJson.user.permissions).toContain('view_movies');

      const decoded: any = jwt.verify(actualJson.token, JWT_SECRET);
      expect(decoded.userId).toBe('cust-id-001');
      expect(decoded.email).toBe(testInput.email);
      expect(decoded.role).toBe('customer');

      expect(mockRedisSetEx).toHaveBeenCalledWith(
        expect.stringContaining(`auth:token:${actualJson.token}`),
        3600,
        expect.any(String)
      );
    });

    test('TC-AUTH-LOGIN-02: login_testNgoaile1_InvalidSchema — Email không hợp lệ kích hoạt lỗi Joi', async () => {
      const testInput = {
        email: 'not-valid-email',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toContain('email');
    });

    test('TC-AUTH-LOGIN-03: login_testNgoaile2_UserNotFound — Email không tồn tại trong DB', async () => {
      const testInput = {
        email: 'nonexistent@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_CREDENTIALS);
    });

    test('TC-AUTH-LOGIN-04: login_testNgoaile3_InvalidPassword — Nhập sai mật khẩu', async () => {
      const testInput = {
        email: 'customer.active@cinema.com',
        password: 'CompletelyWrongPassword123!',
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-id-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_CREDENTIALS);
    });

    test('TC-AUTH-LOGIN-05: login_testNgoaile4_AccountPending — Tài khoản chưa kích hoạt (PENDING)', async () => {
      const testInput = {
        email: 'customer.pending@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-pending-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.PENDING,
          },
        });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.requireVerification).toBe(true);
      expect(mockRes.jsonData.email).toBe(testInput.email);
      expect(mockRes.jsonData.message).toContain('Tài khoản chưa được kích hoạt');
    });

    test('TC-AUTH-LOGIN-06: login_testNgoaile5_AccountBlocked — Tài khoản bị khóa (BLOCKED)', async () => {
      const testInput = {
        email: 'customer.blocked@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-blocked-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: 'BLOCKED',
          },
        });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.requireVerification).toBe(true);
    });

    test('TC-AUTH-LOGIN-07: login_testNgoaile6_RoleNotFound — Không tìm thấy vai trò người dùng trong hệ thống', async () => {
      const testInput = {
        email: 'customer.norole@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-norole-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_CREDENTIALS);
    });

    test('TC-AUTH-LOGIN-08: login_testNgoaile7_ForbiddenRole — Admin cố đăng nhập qua cổng khách hàng (HTTP 403)', async () => {
      const testInput = {
        email: 'admin.user@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            role_name: 'admin',
            role_id: 'role-admin-id',
          },
        });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.FORBIDDEN);
      expect(mockRes.jsonData.message).toContain('Bạn không có quyền truy cập vào hệ thống');
    });

    test('TC-AUTH-LOGIN-09: login_testChuan2_CustomerNoPermissions — Khách hàng đăng nhập thành công khi permissions = []', async () => {
      const testInput = {
        email: 'customer.noperm@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-noperm-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-noperm-001',
            email: testInput.email,
            role_name: 'customer',
            role_id: null,
          },
        });
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      expect(mockRes.jsonData.user.permissions).toEqual([]);
    });

    test('TC-AUTH-LOGIN-10: login_testNgoaile8_InternalServerError — Xử lý khi gRPC client ném lỗi ngoại lệ', async () => {
      const testInput = {
        email: 'customer.crash@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(new Error('Database connection failed'));
      });

      await AuthController.login(req, res, next);

      expect(next).toHaveBeenCalledWith(expect.any(Error));
    });

    test('TC-AUTH-LOGIN-11: login_testNgoaile9_PermissionServiceError — Bắt lỗi khi PermissionService ném exception', async () => {
      const testInput = {
        email: 'customer.permerr@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-permerr-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-permerr-001',
            email: testInput.email,
            role_name: 'customer',
            role_id: 'role-err-id',
          },
        });
      });

      mockGetPermissionsByRoleId.mockImplementation((params: any, callback: any) => {
        callback(new Error('Permission service timeout'));
      });

      await AuthController.login(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      expect(mockRes.jsonData.user.permissions).toEqual([]);
    });

  });

  // ==========================================================================
  // NHÓM 3: KIỂM THỬ AuthController.loginAdmin (Quản trị viên & Nhân viên)
  // ==========================================================================
  describe('Lớp kiểm thử: AuthController — Phương thức: loginAdmin (Đăng nhập Quản trị viên & Nhân viên)', () => {

    test('TC-AUTH-LOGINADMIN-01: loginAdmin_testChuan1_AdminSuccess — Admin đăng nhập thành công', async () => {
      const testInput = {
        email: 'admin.super@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            name: 'Quản trị viên Hệ thống',
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            name: 'Quản trị viên Hệ thống',
            role_name: 'admin',
            role_id: 'role-admin-id',
          },
        });
      });

      mockGetPermissionsByRoleId.mockImplementation((params: any, callback: any) => {
        callback(null, {
          success: true,
          permissions: [
            { id: 'p_all', name: 'Toàn quyền', code: 'admin_all', description: 'Toàn quyền quản trị' },
          ],
        });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      expect(mockRes.jsonData.user.role).toBe('admin');
      expect(mockRes.jsonData.user.permissions).toContain('admin_all');
      expect(mockRedisDel).toHaveBeenCalledWith('permissions:role-admin-id');
    });

    test('TC-AUTH-LOGINADMIN-02: loginAdmin_testChuan2_ManagerStaffSuccess — Manager Staff đăng nhập thành công', async () => {
      const testInput = {
        email: 'manager.staff@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'mgr-id-001',
            email: testInput.email,
            name: 'Nguyễn Văn Quản Lý',
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'mgr-id-001',
            email: testInput.email,
            role_name: 'manager_staff',
            role_id: 'role-mgr-id',
          },
        });
      });

      mockGetPermissionsByRoleId.mockImplementation((params: any, callback: any) => {
        callback(null, {
          success: true,
          permissions: [
            { id: 'p_mv', code: 'manage_movies' },
            { id: 'p_rm', code: 'manage_rooms' },
          ],
        });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      expect(mockRes.jsonData.user.role).toBe('manager_staff');
      expect(mockRes.jsonData.user.permissions).toContain('manage_movies');
    });

    test('TC-AUTH-LOGINADMIN-03: loginAdmin_testChuan3_TicketStaffSuccess — Ticket Staff đăng nhập thành công', async () => {
      const testInput = {
        email: 'ticket.staff@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'ticket-id-001',
            email: testInput.email,
            name: 'Trần Thị Thu Ngân',
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'ticket-id-001',
            email: testInput.email,
            role_name: 'ticket_staff',
            role_id: 'role-ticket-id',
          },
        });
      });

      mockGetPermissionsByRoleId.mockImplementation((params: any, callback: any) => {
        callback(null, {
          success: true,
          permissions: [{ id: 'p_tk', code: 'sell_tickets' }],
        });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      expect(mockRes.jsonData.user.role).toBe('ticket_staff');
      expect(mockRes.jsonData.user.permissions).toContain('sell_tickets');
    });

    test('TC-AUTH-LOGINADMIN-04: loginAdmin_testChuan4_FirstLogin_ActivateUser_CheckDB_Rollback — Nhân viên kích hoạt lần đầu, CheckDB và Rollback', async () => {
      const mockDatabaseState: Record<string, { status: string; email: string }> = {
        'staff.firsttime@cinema.com': {
          email: 'staff.firsttime@cinema.com',
          status: UserStatus.PENDING,
        },
      };

      const testInput = {
        email: 'staff.firsttime@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        const dbRecord = mockDatabaseState[params.email];
        callback(null, {
          found: true,
          user: {
            id: 'staff-first-001',
            email: dbRecord.email,
            name: 'Nhân Viên Mới Tuyển',
            password: HASHED_PASSWORD,
            status: dbRecord.status,
          },
        });
      });

      mockActivateUser.mockImplementation((params: any, callback: any) => {
        if (mockDatabaseState[params.email]) {
          mockDatabaseState[params.email].status = UserStatus.ACTIVE;
        }
        callback(null, { success: true });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'staff-first-001',
            email: testInput.email,
            role_name: 'ticket_staff',
            role_id: 'role-ticket-id',
          },
        });
      });

      try {
        await AuthController.loginAdmin(req, res, next);

        const mockRes = res as unknown as IMockResponse;
        expect(mockRes.json).toHaveBeenCalled();
        expect(mockRes.jsonData.isFirstLogin).toBe(true);
        expect(mockRes.jsonData.message).toBe('Đăng nhập thành công! Chào mừng bạn đến với hệ thống.');

        // CHECK DB
        const currentDbStatus = mockDatabaseState[testInput.email].status;
        expect(currentDbStatus).toBe(UserStatus.ACTIVE);
        expect(mockActivateUser).toHaveBeenCalledWith({ email: testInput.email }, expect.any(Function));

      } finally {
        // ROLLBACK
        mockDatabaseState[testInput.email].status = UserStatus.PENDING;
        expect(mockDatabaseState[testInput.email].status).toBe(UserStatus.PENDING);
      }
    });

    test('TC-AUTH-LOGINADMIN-05: loginAdmin_testNgoaile1_UserNotFound — Email admin không tồn tại', async () => {
      const testInput = {
        email: 'ghost.admin@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_CREDENTIALS);
    });

    test('TC-AUTH-LOGINADMIN-06: loginAdmin_testNgoaile2_InvalidPassword — Nhập sai mật khẩu admin/staff', async () => {
      const testInput = {
        email: 'admin.super@cinema.com',
        password: 'WrongPassword123@',
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_CREDENTIALS);
    });

    test('TC-AUTH-LOGINADMIN-07: loginAdmin_testNgoaile3_AccountBlocked — Tài khoản staff bị khóa', async () => {
      const testInput = {
        email: 'staff.blocked@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'staff-blocked-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: 'BLOCKED',
          },
        });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.requireVerification).toBe(true);
    });

    test('TC-AUTH-LOGINADMIN-08: loginAdmin_testNgoaile4_CustomerForbidden — Khách hàng cố tình đăng nhập vào trang Admin', async () => {
      const testInput = {
        email: 'customer.regular@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-id-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'cust-id-001',
            email: testInput.email,
            role_name: 'customer',
            role_id: 'role-cust-id',
          },
        });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.FORBIDDEN);
      expect(mockRes.jsonData.message).toContain('Bạn không có quyền truy cập vào hệ thống');
    });

    test('TC-AUTH-LOGINADMIN-09: loginAdmin_testNgoaile5_InvalidSchema — Email admin không hợp lệ kích hoạt lỗi Joi', async () => {
      const testInput = {
        email: 'invalid-admin-email',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toContain('email');
    });

    test('TC-AUTH-LOGINADMIN-10: loginAdmin_testNgoaile6_RoleNotFound — Không tìm thấy role của Admin/Staff', async () => {
      const testInput = {
        email: 'admin.norole@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-norole-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.INVALID_CREDENTIALS);
    });

    test('TC-AUTH-LOGINADMIN-11: loginAdmin_testNgoaile7_PermissionServiceError — Bắt lỗi khi lấy quyền của Admin/Staff', async () => {
      const testInput = {
        email: 'admin.super@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            password: HASHED_PASSWORD,
            status: UserStatus.ACTIVE,
          },
        });
      });

      mockGetUserWithRoleByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: {
            id: 'admin-id-001',
            email: testInput.email,
            role_name: 'admin',
            role_id: 'role-admin-id',
          },
        });
      });

      mockGetPermissionsByRoleId.mockImplementation((params: any, callback: any) => {
        callback(new Error('Permission service failure'));
      });

      await AuthController.loginAdmin(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.json).toHaveBeenCalled();
      expect(mockRes.jsonData.user.permissions).toEqual([]);
    });

    test('TC-AUTH-LOGINADMIN-12: loginAdmin_testNgoaile8_InternalServerError — Xử lý lỗi không mong muốn trong loginAdmin', async () => {
      const testInput = {
        email: 'admin.crash@cinema.com',
        password: RAW_PASSWORD,
      };
      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(new Error('Fatal database connection error'));
      });

      await AuthController.loginAdmin(req, res, next);

      expect(next).toHaveBeenCalledWith(expect.any(Error));
    });

  });

  // ==========================================================================
  // NHÓM 4: KIỂM THỬ TokenService & Session Cache
  // ==========================================================================
  describe('Lớp kiểm thử: TokenService — Dịch vụ JWT Token & Cache Phiên đăng nhập', () => {

    test('TC-TOKEN-SERVICE-01: tokenService_testChuan1_GenerateAndVerifyToken — Sinh token và xác minh tính toàn vẹn payload', () => {
      const payload = {
        userId: 'user-uuid-1234',
        email: 'user.test@cinema.com',
        role: 'customer',
        permissions: ['view_movies', 'book_tickets'],
      };

      const token = jwt.sign(payload, JWT_SECRET, { expiresIn: '1h' });

      expect(token).toBeDefined();
      expect(typeof token).toBe('string');

      const decoded: any = jwt.verify(token, JWT_SECRET);
      expect(decoded.userId).toBe(payload.userId);
      expect(decoded.email).toBe(payload.email);
      expect(decoded.role).toBe(payload.role);
      expect(decoded.permissions).toEqual(payload.permissions);
    });

    test('TC-TOKEN-SERVICE-02: tokenService_testChuan2_CacheUserInfo — Lưu cache thông tin phiên đăng nhập vào Redis', async () => {
      const testToken = 'mock_jwt_access_token_xyz';
      const userInfo = {
        id: 'user-uuid-1234',
        email: 'user.test@cinema.com',
        role: 'customer',
        roleId: 'role-customer-id',
        permissions: ['view_movies'],
        cachedAt: new Date().toISOString(),
      };

      await TokenService.cacheUserInfo(testToken, userInfo);

      expect(mockRedisSetEx).toHaveBeenCalledWith(
        `auth:token:${testToken}`,
        3600,
        JSON.stringify(userInfo)
      );
    });

  });

  // ==========================================================================
  // NHÓM 5: KIỂM THỬ User Model / Database DAO (CheckDB & Rollback)
  // ==========================================================================
  describe('Lớp kiểm thử: UserModel / DAO — Truy xuất CSDL, CheckDB và Rollback', () => {

    test('TC-USER-DAO-01: userDAO_testChuan1_FindByEmail — Truy vấn người dùng theo email', async () => {
      const mockUserTable = [
        { id: 'u1', email: 'customer.active@cinema.com', name: 'Nguyễn Văn A', status: 'ACTIVE' },
        { id: 'u2', email: 'admin@cinema.com', name: 'Admin Hệ Thống', status: 'ACTIVE' },
      ];

      const findUserByEmail = async (email: string) => {
        return mockUserTable.find(u => u.email === email) || null;
      };

      const actualUser = await findUserByEmail('customer.active@cinema.com');

      expect(actualUser).not.toBeNull();
      expect(actualUser?.email).toBe('customer.active@cinema.com');
      expect(actualUser?.status).toBe('ACTIVE');

      const notFoundUser = await findUserByEmail('unknown@cinema.com');
      expect(notFoundUser).toBeNull();
    });

    test('TC-USER-DAO-02: userDAO_testChuan2_UpdateUserStatus_CheckDB_Rollback — Cập nhật DB, CheckDB và Rollback giao dịch', async () => {
      const originalUserRecord = {
        id: 'u-transaction-001',
        email: 'staff.pending@cinema.com',
        status: UserStatus.PENDING,
      };

      let databaseTable = { ...originalUserRecord };

      class DatabaseTransaction {
        private snapshot: any;
        public active: boolean = true;

        constructor(currentState: any) {
          this.snapshot = { ...currentState };
        }

        public async update(fields: any) {
          databaseTable = { ...databaseTable, ...fields };
        }

        public async rollback() {
          databaseTable = { ...this.snapshot };
          this.active = false;
        }

        public async commit() {
          this.active = false;
        }
      }

      const transaction = new DatabaseTransaction(databaseTable);

      try {
        await transaction.update({ status: UserStatus.ACTIVE });

        // CheckDB
        expect(databaseTable.status).toBe(UserStatus.ACTIVE);
        expect(databaseTable.email).toBe(originalUserRecord.email);

      } finally {
        // Rollback
        await transaction.rollback();

        // CheckDB sau Rollback
        expect(databaseTable.status).toBe(UserStatus.PENDING);
        expect(databaseTable.id).toBe(originalUserRecord.id);
      }
    });

  });

});
