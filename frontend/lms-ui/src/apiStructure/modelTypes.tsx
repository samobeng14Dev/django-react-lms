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

// export interface CartStats {
// 	total_price: number;
// 	total_tax: number;
// 	total_total: number;
// 	price: number;
// 	total: number;
//     tax: number; 
// }

export interface CartListItem {
	id: number;
	price: string;
	tax_fee: string;
	total: string;
	country: string;
	cart_id: string;
	date: string;
	course: Course;
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
}

export interface Student {
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
	groups: any[]; // Update this if you know the shape of group objects
	user_permissions: any[]; // Update this if you know the shape of permission objects
}

export interface Order {
	id: number;
	sub_total: string;
	tax_fee: string;
	total: string;
	initial_total: string;
	saved: string;
	payment_status: string;
	full_name: string;
	email: string;
	country: string;
	stripe_session_id: string | null;
	oid: string;
	date: string;
	student: Student;
	teachers: Teacher[];
}

export interface OrderItem {
	id: number;
	price: string;
	tax_fee: string;
	total: string;
	initial_total: string;
	saved: string;
	applied_coupon: boolean;
	oid: string;
	date: string;
	order: Order;
}

export interface OrderResponse {
	id: number;
	order_items: OrderItem[];
}
