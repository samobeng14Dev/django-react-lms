export interface Category {
  id: number;
  title: string;
  image: string;
  active: boolean;
  slug: string;
}

export interface User {
  id: number;
  password: string;
  last_login: string;
  is_superuser: boolean;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
  username: string;
  email: string;
  full_name: string;
  otp: string;
  refresh_token: string;
  groups: any[]; 
  user_permissions: any[];
}

export interface Teacher {
  id: number;
  image: string;
  full_name: string;
  bio: string;
  facebook: string | null;
  twitter: string | null;
  linkedin: string | null;
  about: string;
  country: string;
  user: User;
}

export interface Course {
  id: number;
  category: Category;
  teacher: Teacher;
  file: string;
  image: string;
  title: string;
  description: string;
  price: string;
  language: string;
  level: string;
  platform_status: string;
  teacher_course_status: string;
  featured: boolean;
  course_id: string;
  slug: string;
  date: string;
  students: any[];
  curriculum: any[];
  lectures: any[];
  average_rating: number | null;
  rating_count: number;
  reviews: any[];
}
export interface Cart {
  price: string;
	tax_fee: string; 
	total: string; 
	country?: string | null; 
	cart_id: string;
	date: string;
}
