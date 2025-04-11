function CartID(): string {
	const length = 6;
	const characters = '1234567890';
	let randomString = localStorage.getItem("randomString");

	if (!randomString) {
		randomString = "";
		for (let i = 0; i < length; i++) {
			const randomIndex = Math.floor(Math.random() * characters.length);
			randomString += characters.charAt(randomIndex);
		}
		localStorage.setItem("randomString", randomString);
	}

	return randomString;
}

export default CartID;
