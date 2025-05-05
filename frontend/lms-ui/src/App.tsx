import { useState, useEffect } from "react";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import MainWrapper from "./Layouts/MainWrapper";
import PrivateRoute from "./Layouts/PrivateRoute";
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout";
import ForgotPassword from "./views/auth/ForgotPassword";
import CreateNewPassword from "./views/auth/CreateNewPassword";
import StudentChangePassword from "./views/student/ChangePassword";
import StudentDashboard from "./views/student/Dashboard"; 
import Index from "./views/base/Index";
import CourseDetail from "./views/base/CourseDetail";
import StudentCourses from "./views/student/Courses";
import StudentCourseDetail from "./views/student/CourseDetail";
import Cart from "./views/base/Cart";
import { CartContext, ProfileContext } from "./views/plugin/Context";
import apiInstance from "./utils/axios";
import UserData from "./views/plugin/UserData";
import CartID from "./views/plugin/CartID";
import useAxios from "./utils/useAxios";
import Checkout from "./views/base/Checkout";
import Wishlist from "./views/student/Wishlist";
import StudentProfile from "./views/student/Profile";

const App: React.FC = () => {
	const [cartCount, setCartCount] = useState(0);
	const [profile, setProfile] = useState<any>([]);

	useEffect(() => {
		apiInstance.get(`course/cart-list/${CartID()}/`).then((res) => {
			setCartCount(res.data?.length);
		});

		useAxios().get(`user/profile/${UserData()?.user_id}/`).then((res) => {
			setProfile(res.data);
		});
	}, []);

	

	return (
		<CartContext.Provider value={[cartCount, setCartCount]}>
			<ProfileContext.Provider value={[profile, setProfile]}>
				<BrowserRouter>
					<MainWrapper>
						<Routes>
							<Route
								path='/register/'
								element={<Register />}
							/>
							<Route
								path='/login/'
								element={<Login />}
							/>
							<Route
								path='/logout/'
								element={<Logout />}
							/>
							<Route
								path='/forgot-password/'
								element={<ForgotPassword />}
							/>
							<Route
								path='/create-new-password/'
								element={<CreateNewPassword />}
							/>

							{/* Base Routes */}
							<Route
								path='/'
								element={<Index />}
							/>
							<Route
								path='/course-detail/:slug/'
								element={<CourseDetail />}
							/>
							<Route
								path='/cart/'
								element={<Cart />}
							/>
							<Route
								path='/checkout/:order_oid/'
								element={<Checkout />}
							/>
							{/* <Route
								path='/payment-success/:order_oid/'
								element={<Success />}
							/>
							<Route
								path='/search/'
								element={<Search />}
							/> */}

							{/* Student Routes */}
							<Route
								path='/student/dashboard/'
								element={
									<PrivateRoute>
										<StudentDashboard />
									</PrivateRoute>
								}
							/>
							<Route
								path='/student/courses/'
								element={
									<PrivateRoute>
										<StudentCourses />
									</PrivateRoute>
								}
							/>
							<Route
								path='/student/courses/:enrollment_id/'
								element={
									<PrivateRoute>
										<StudentCourseDetail />
									</PrivateRoute>
								}
							/>
							<Route
								path='/student/wishlist/'
								element={
									<PrivateRoute>
										<Wishlist />
									</PrivateRoute>
								}
							/>
							<Route
								path='/student/profile/'
								element={
									<PrivateRoute>
										<StudentProfile />
									</PrivateRoute>
								}
							/>
							<Route
								path='/student/change-password/'
								element={
									<PrivateRoute>
										<StudentChangePassword />
									</PrivateRoute>
								}
							/>

							{/* Teacher Routes */}
							

						
						</Routes>
					</MainWrapper>
				</BrowserRouter>
			</ProfileContext.Provider>
		</CartContext.Provider>
	);
};

export default App;
