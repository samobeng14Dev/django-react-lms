import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import { register } from "../../utils/auth";

function Register() {
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password1: "",
    password2: "",
  });

  const [loading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // Handles input change dynamically
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const { error } = await register(formData);
      if (!error) {
        Swal.fire("Success", "Registration Successful", "success");
        navigate("/");
      } else {
        Swal.fire("Error", error, "error");
      }
    } catch (error) {
      Swal.fire("Error", "An unexpected error occurred", "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <BaseHeader />
      <section className="container d-flex flex-column vh-100" style={{ marginTop: "150px" }}>
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Sign up</h1>
                  <span>
                    Already have an account?
                    <Link to="/login/" className="ms-1">Sign In</Link>
                  </span>
                </div>
                {/* Form */}
                <form className="needs-validation" noValidate onSubmit={handleSubmit}>
                  {/* Full Name */}
                  <div className="mb-3">
                    <label htmlFor="full_name" className="form-label">Full Name</label>
                    <input
                      type="text"
                      id="full_name"
                      className="form-control"
                      name="full_name"
                      placeholder="John Doe"
                      required
                      value={formData.full_name}
                      onChange={handleChange}
                    />
                  </div>
                  {/* Email */}
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      name="email"
                      placeholder="johndoe@gmail.com"
                      required
                      value={formData.email}
                      onChange={handleChange}
                    />
                  </div>
                  {/* Password */}
                  <div className="mb-3">
                    <label htmlFor="password1" className="form-label">Password</label>
                    <input
                      type="password"
                      id="password1"
                      className="form-control"
                      name="password1"
                      placeholder="**************"
                      required
                      value={formData.password1}
                      onChange={handleChange}
                    />
                  </div>
                  {/* Confirm Password */}
                  <div className="mb-3">
                    <label htmlFor="password2" className="form-label">Confirm Password</label>
                    <input
                      type="password"
                      id="password2"
                      className="form-control"
                      name="password2"
                      placeholder="**************"
                      required
                      value={formData.password2}
                      onChange={handleChange}
                    />
                  </div>
                  {/* Submit Button */}
                  <div className="d-grid">
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                      {loading ? "Signing Up..." : "Sign Up"} <i className="fas fa-user-plus"></i>
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
}

export default Register;
