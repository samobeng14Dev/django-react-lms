import { useState, useEffect } from "react";

type Address = {
  country?: string;
  [key: string]: any; // for other address fields (like city, road, etc.)
};

function useCurrentAddress() {
  const [address, setAddress] = useState<Address | null>(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((pos) => {
      const { latitude, longitude } = pos.coords;

      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`;

      fetch(url)
        .then((res) => res.json())
        .then((data) => setAddress(data.address));
    });
  }, []);

  return address;
}

export default useCurrentAddress;
