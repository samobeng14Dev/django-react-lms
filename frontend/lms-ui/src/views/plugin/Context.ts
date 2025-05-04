// import { createContext } from "react";

// export const CartContext = createContext(null);



import { createContext, Dispatch, SetStateAction } from "react";

export type CartContextType = [number, Dispatch<SetStateAction<number>>];
export const CartContext = createContext<CartContextType | null>(null);
 export const ProfileContext = createContext<any>(null);