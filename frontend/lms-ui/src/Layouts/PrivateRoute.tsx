import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'


import React from 'react'

import { ReactNode } from 'react';

const PrivateRoute=({children}: { children: ReactNode })=> {
    const loggedIn = useAuthStore(state => state.isLoggedIn)()
    
    return loggedIn ? <>{ children}</>:<Navigate to='/login'/>
} 

export default PrivateRoute