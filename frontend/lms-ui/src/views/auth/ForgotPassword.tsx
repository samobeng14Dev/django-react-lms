import React from 'react';
import BaseHeader from '../partials/BaseHeader';
import BaseFooter from '../partials/BaseFooter';
import { useFormik } from 'formik';
import * as Yup from "yup";
import apiInstance from '../../utils/axios';


const ForgotPassword: React.FC = () => {
  
  const formik = useFormik({
    initialValues: {
      email: ''
    },
    validationSchema: Yup.object({
      email: Yup.string().email('Invalid email address').required('Required')
    }),
    onSubmit: async (values, { setSubmitting }) => {
      try {
        await apiInstance.get(`/user/password-reset/${values}`);
       
      } catch (error) {
       
      }
      setSubmitting(false);
    }
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
                  <h1 className="mb-1 fw-bold">Forgot Password</h1>
                  <span>
                    Let's help you get back into your account
                  </span>
                </div>

                <form className="needs-validation" noValidate onSubmit={formik.handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      className={`form-control ${formik.touched.email && formik.errors.email ? 'is-invalid' : ''}`}
                      placeholder="johndoe@gmail.com"
                      {...formik.getFieldProps('email')}
                      required
                    />
                    {formik.touched.email && formik.errors.email ? (
                      <div className="invalid-feedback">{formik.errors.email}</div>
                    ) : null}
                  </div>

                  <div className="d-grid">
                    <button type="submit" className="btn btn-primary" disabled={formik.isSubmitting}>
                      {formik.isSubmitting ? 'Sending...' : 'Reset Password'} <i className='fas fa-arrow-right'></i>
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

export default ForgotPassword;
