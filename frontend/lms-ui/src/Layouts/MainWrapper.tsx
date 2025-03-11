import React, { useEffect, useState, ReactNode } from "react";
import { setUser } from "../utils/auth";

const MainWrapper = ({ children }: { children: ReactNode }) => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const handler = async () => {
            setLoading(true)

            await setUser()
            setLoading(false)
        }
        handler()
    }, [])
    
    return <>{loading ? null : children}</>
    
}

export default MainWrapper