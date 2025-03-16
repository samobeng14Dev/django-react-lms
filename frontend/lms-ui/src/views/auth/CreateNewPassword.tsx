import React from "react";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import { useNavigate,useSearchParams } from "react-router-dom";
import apiInstance from "../../utils/axios";
import * as Yup from "yup";
import Swal from "sweetalert2";
import { FormikHelpers, useFormik } from "formik";

interface CreatePasswordValues {
  password: string;
  confirmPassword: string;
}

const CreateNewPassword: React.FC = () => {
  const navigate: ReturnType<typeof useNavigate> = useNavigate();
  const [searchParams] = useSearchParams()
  const otp = searchParams.get("otp")
  const uuidb64 = searchParams.get("uuidb64")
  const refresh_token=searchParams.get("refresh_token")

  const validationSchema = Yup.object({
    password: Yup.string()
      .min(8, "Password must be at least 8 characters")
      .required("Password is required"),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref("password")], "Passwords must match")
      .required("Confirm Password is required"),
  });

  const formik = useFormik<CreatePasswordValues>({
    initialValues: {
      password: "",
      confirmPassword: "",
    },
    validationSchema,
    onSubmit: async(values, { setSubmitting }: FormikHelpers<CreatePasswordValues>) => {
      try {
         const payload = {
        ...values,
        otp,
        uuidb64,
        refresh_token,
      };
        await apiInstance.post("/user/password-change", payload);
        Swal.fire("Success", "Password Changed Successful", "success");
        navigate("/login"); // Redirect after success
      } catch (error) {
        console.log(error);
        Swal.fire("Error", "An unexpected error occurred", "error");
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <>
      <BaseHeader />

      <section
        className="container d-flex flex-column vh-100"
        style={{ marginTop: "150px" }}
      >
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Create New Password</h1>
                  <span>Choose a new password for your account</span>
                </div>

                <form className="needs-validation" noValidate onSubmit={formik.handleSubmit}>
                  {/* Password Field */}
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Enter New Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className={`form-control ${formik.touched.password && formik.errors.password ? "is-invalid" : ""}`}
                      placeholder="**************"
                      {...formik.getFieldProps("password")}
                    />
                    {formik.touched.password && formik.errors.password ? (
                      <div className="invalid-feedback">{formik.errors.password}</div>
                    ) : null}
                  </div>

                  {/* Confirm Password Field */}
                  <div className="mb-3">
                    <label htmlFor="confirmPassword" className="form-label">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="confirmPassword"
                      className={`form-control ${formik.touched.confirmPassword && formik.errors.confirmPassword ? "is-invalid" : ""}`}
                      placeholder="**************"
                      {...formik.getFieldProps("confirmPassword")}
                    />
                    {formik.touched.confirmPassword && formik.errors.confirmPassword ? (
                      <div className="invalid-feedback">{formik.errors.confirmPassword}</div>
                    ) : null}
                  </div>

                  {/* Submit Button with Loading Indicator */}
                  <div>
                    <div className="d-grid">
                      <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={formik.isSubmitting}
                      >
                        {formik.isSubmitting ? (
                          <>
                            <i className="fas fa-spinner fa-spin"></i> Saving...
                          </>
                        ) : (
                          <>
                            Save New Password <i className="fas fa-check-circle"></i>
                          </>
                        )}
                      </button>
                    </div>
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

export default CreateNewPassword;
