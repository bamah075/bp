import { Request, Response } from 'express';
import { ApiError } from '../middleware/errorHandler';
import { AuthService } from '../services/authService';
import { UserRepository } from '../repositories/userRepository';
import { CreateUserRequest, AuthPayload, TokenPayload } from '../types/api';

export class AuthController {
  static async register(req: Request, res: Response) {
    const { email, password, full_name } = req.body as CreateUserRequest;

    if (!email || !password || !full_name) {
      throw new ApiError(400, 'Email, password, and full_name are required');
    }

    const emailExists = await UserRepository.emailExists(email);
    if (emailExists) {
      throw new ApiError(409, 'Email already registered');
    }

    const user = await UserRepository.create(email, password, full_name);

    const tokens = AuthService.generateTokenPair({
      id: user.id,
      email: user.email,
      role: user.role,
    });

    res.status(201).json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          full_name: user.full_name,
          role: user.role,
          avatar_url: user.avatar_url,
        },
        tokens,
      },
    });
  }

  static async login(req: Request, res: Response) {
    const { email, password } = req.body as AuthPayload;

    if (!email || !password) {
      throw new ApiError(400, 'Email and password are required');
    }

    const user = await UserRepository.findByEmail(email);
    if (!user) {
      throw new ApiError(401, 'Invalid credentials');
    }

    const passwordMatch = await AuthService.verifyPassword(password, user.password_hash);
    if (!passwordMatch) {
      throw new ApiError(401, 'Invalid credentials');
    }

    if (user.status !== 'active') {
      throw new ApiError(403, 'User account is not active');
    }

    const tokens = AuthService.generateTokenPair({
      id: user.id,
      email: user.email,
      role: user.role,
    });

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          full_name: user.full_name,
          role: user.role,
          avatar_url: user.avatar_url,
        },
        tokens,
      },
    });
  }

  static async refresh(req: Request, res: Response) {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      throw new ApiError(400, 'Refresh token is required');
    }

    try {
      const payload = AuthService.verifyRefreshToken(refreshToken);
      const user = await UserRepository.findById(payload.id);

      if (!user || user.status !== 'active') {
        throw new ApiError(403, 'User is not active');
      }

      const tokens = AuthService.generateTokenPair({
        id: user.id,
        email: user.email,
        role: user.role,
      });

      res.status(200).json({
        success: true,
        data: { tokens },
      });
    } catch (error) {
      throw new ApiError(401, 'Invalid refresh token');
    }
  }

  static async logout(req: Request, res: Response) {
    res.status(200).json({
      success: true,
      data: { message: 'Logged out successfully' },
    });
  }
}
