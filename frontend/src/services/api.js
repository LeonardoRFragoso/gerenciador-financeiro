/**
 * Configuração da API para integração com o backend Django
 * Finance Control - API Service
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configuração base do axios ou fetch
class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  // Headers padrão para requisições
  getHeaders(includeAuth = true) {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (includeAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Método genérico para fazer requisições
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(options.auth !== false),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      // Se token expirou, tentar renovar
      if (response.status === 401 && this.token) {
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Tentar novamente com novo token
          config.headers['Authorization'] = `Bearer ${this.token}`;
          return await fetch(url, config);
        } else {
          // Redirecionar para login
          this.logout();
          throw new Error('Token expirado. Faça login novamente.');
        }
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }

  // Auth methods
  async login(email, password) {
    const response = await this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    return response;
  }

  async register(userData) {
    const response = await this.request('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
    return response;
  }

  async logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await this.request('/auth/logout/', {
        method: 'POST',
        body: JSON.stringify({ refresh: refreshToken })
      });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async forgotPassword(email) {
    const response = await this.request('/auth/password-reset/', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
    return response;
  }

  async resetPassword(token, password) {
    const response = await this.request('/auth/password-reset-confirm/', {
      method: 'POST',
      body: JSON.stringify({ token, password })
    });
    return response;
  }

  async getCurrentUser() {
    const response = await this.request('/auth/user/');
    return response;
  }

  async updateProfile(profileData) {
    const response = await this.request('/auth/user/', {
      method: 'PATCH',
      body: JSON.stringify(profileData)
    });
    return response;
  }

  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) return false;

      const response = await this.request('/auth/refresh/', {
        method: 'POST',
        body: JSON.stringify({ refresh: refreshToken }),
        auth: false,
      });

      if (response.access) {
        this.token = response.access;
        localStorage.setItem('access_token', response.access);
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
    return false;
  }



  // Usuários
  async getUserProfile() {
    return this.request('/accounts/profile/');
  }

  async updateUserProfile(data) {
    return this.request('/accounts/profile/', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }



  // Transações
  async getTransactions(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/transactions/transactions/${queryString ? `?${queryString}` : ''}`);
  }

  async createTransaction(data) {
    return this.request('/transactions/transactions/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTransaction(id, data) {
    return this.request(`/transactions/transactions/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteTransaction(id) {
    return this.request(`/transactions/transactions/${id}/`, {
      method: 'DELETE',
    });
  }

  async getTransactionSummary(startDate, endDate) {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return this.request(`/transactions/summary/?${params.toString()}`);
  }

  async getMonthlyReport() {
    return this.request('/transactions/monthly-report/');
  }

  async getCategoriesReport(type = 'expense') {
    return this.request(`/transactions/categories-report/?type=${type}`);
  }

  // Metas
  async getGoals(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/goals/goals/${queryString ? `?${queryString}` : ''}`);
  }

  async createGoal(data) {
    return this.request('/goals/goals/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateGoal(id, data) {
    return this.request(`/goals/goals/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteGoal(id) {
    return this.request(`/goals/goals/${id}/`, {
      method: 'DELETE',
    });
  }

  async contributeToGoal(goalId, amount, description = '') {
    return this.request(`/goals/${goalId}/contribute/`, {
      method: 'POST',
      body: JSON.stringify({ amount, description }),
    });
  }

  async getGoalSummary() {
    return this.request('/goals/summary/');
  }

  // Categorias
  async getCategories(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/categories/categories/${queryString ? `?${queryString}` : ''}`);
  }

  async getCategoriesByType() {
    return this.request('/categories/categories/by_type/');
  }

  async createCategory(data) {
    return this.request('/categories/categories/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateCategory(id, data) {
    return this.request(`/categories/categories/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteCategory(id) {
    return this.request(`/categories/categories/${id}/`, {
      method: 'DELETE',
    });
  }

  async createDefaultCategories() {
    return this.request('/categories/defaults/', {
      method: 'POST',
    });
  }
}

// Instância singleton da API
const apiService = new ApiService();

export default apiService;
