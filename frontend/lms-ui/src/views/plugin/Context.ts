// import { createContext } from "react";

// export const CartContext = createContext(null);

// export const ProfileContext = createContext(null);

import { createContext, Dispatch, SetStateAction } from "react";

export type CartContextType = [number, Dispatch<SetStateAction<number>>];
export const CartContext = createContext<CartContextType | null>(null);