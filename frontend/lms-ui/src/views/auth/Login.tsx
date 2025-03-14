import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import { Link, useNavigate } from "react-router-dom";
import { useFormik, FormikHelpers } from "formik";
import * as Yup from "yup";
import { login } from "../../utils/auth";
import Swal from "sweetalert2";

// Define the form values type
interface LoginFormValues {
  email: string;
  password: string;
}

const Login: React.FC = () => {
  const navigate: ReturnType<typeof useNavigate> = useNavigate();

  // Validation Schema
  const validationSchema = Yup.object({
    email: Yup.string()
      .email("Invalid email address")
      .required("Email is required"),
    password: Yup.string()
      .min(8, "Password must be at least 8 characters")
      // .matches(/[A-Z]/, "Must contain at least one uppercase letter")
      // .matches(/[a-z]/, "Must contain at least one lowercase letter")
      // .matches(/\d/, "Must contain at least one number")
      // .matches(/[!@#$%^&*(),.?":{}|<>]/, "Must contain one special character")
      .required("Password is required"),
  });

  // Formik
  const formik = useFormik<LoginFormValues>({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema,
    onSubmit: async (values: LoginFormValues, { setSubmitting }: FormikHelpers<LoginFormValues>) => {
      try {
        const { error } = await login(values);
        if (!error) {
          Swal.fire("Success", "Login Successful", "success");
          navigate("/");
        } else {
          Swal.fire("Error", error, "error");
        }
      } catch (error) {
        Swal.fire("Error", "An unexpected error occurred", "error");
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <>
      <BaseHeader />

      <section className="container d-flex flex-column vh-100" style={{ marginTop: "150px" }}>
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Sign in</h1>
                  <span>
                    Don’t have an account?
                    <Link to="/register/" className="ms-1">Sign up</Link>
                  </span>
                </div>
                
                {/* Form */}
                <form className="needs-validation" noValidate onSubmit={formik.handleSubmit}>
                  {/* Email */}
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      className={`form-control ${formik.touched.email && formik.errors.email ? "is-invalid" : ""}`}
                      {...formik.getFieldProps("email")}
                      placeholder="johndoe@gmail.com"
                      required
                    />
                    {formik.touched.email && formik.errors.email && (
                      <div className="invalid-feedback">{formik.errors.email}</div>
                    )}
                  </div>

                  {/* Password */}
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                      type="password"
                      id="password"
                      className={`form-control ${formik.touched.password && formik.errors.password ? "is-invalid" : ""}`}
                      {...formik.getFieldProps("password")}
                      placeholder="**************"
                      required
                    />
                    {formik.touched.password && formik.errors.password && (
                      <div className="invalid-feedback">{formik.errors.password}</div>
                    )}
                  </div>

                  {/* Checkbox */}
                  <div className="d-lg-flex justify-content-between align-items-center mb-4">
                    <div className="form-check">
                      <input type="checkbox" className="form-check-input" id="rememberme" />
                      <label className="form-check-label" htmlFor="rememberme">Remember me</label>
                    </div>
                    <div>
                      <Link to="/forgot-password/">Forgot your password?</Link>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <div className="d-grid">
                    <button type="submit" className="btn btn-primary" disabled={formik.isSubmitting}>
                      {formik.isSubmitting ? "Signing in..." : "Sign in"} <i className="fas fa-sign-in-alt"></i>
                    </button>
                  </div>
                </form>

              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
};

export default Login;
