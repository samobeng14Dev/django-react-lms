import Cookie from "js-cookie";
import jwtDecode from "jwt-decode";

function UserData(): any {
	let access_token = Cookie.get("access_token");
	let refresh_token = Cookie.get("refresh_token");

	if (access_token && refresh_token) {
    const decoded = jwtDecode(access_token); // <-- use access_token here
    console.log("Decoded User Data:", decoded);
    
		return decoded;
	}

	return null;
}

export default UserData;
