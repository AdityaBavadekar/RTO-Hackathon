// import React, { useEffect } from "react";
// import tt from "@tomtom-international/web-sdk-maps";
// import "@tomtom-international/web-sdk-maps/dist/maps.css";
// import type { Challan } from "../types";

// interface MapViewProps {
//   challans: Challan[];
// }

// const MapView: React.FC<MapViewProps> = () => {
//   const mapElement = React.useRef<HTMLDivElement>(null);
//   const [map, setMap] = React.useState<tt.Map | null>(null);
//   const [challans, setChallans] = React.useState<Challan[]>([]);

//   useEffect(() => {
//     fetch("http://192.168.58.4:8000/api/rto/incidents", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         rto_id: localStorage.getItem("rto_id") || 0,
//       }),
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         setChallans(
//           data["incidents"].map((challan: any) => ({
//             vehicleNumber: challan.incident_vin,
//             time_stamp: challan.challans[0].challan_timestamp,
//             amount: challan.challans[0].challan_amount,
//             location: {
//               lat: challan.incident_lat,
//               lng: challan.incident_long,
//             },
//           }))
//         );
//         console.log("Challans", challans);
//       });
//   }, []);

//   React.useEffect(() => {
//     if (!mapElement.current) return;

//     const map = tt.map({
//       key: "jFf7r7QHWdsF8AFHXCz3Gvbm6kh7uX0j",
//       container: mapElement.current,
//       center: [-122.4194, 37.7749],
//       zoom: 12,
//     });

//     setMap(map);

//     new tt.Marker()
//       .setLngLat([-122.4194, 37.7749]) // Correct order: [lng, lat]
//       .addTo(map);

//     return () => map.remove();
//   }, []);

//   React.useEffect(() => {
//     if (!map) return;

//     challans.forEach((challan) => {
//       const popup = new tt.Popup({ offset: 30 }).setHTML(`
//         <div class="p-2">
//           <h3 class="font-bold">${challan.vehicleNumber}</h3>
//           <p>${challan.time_stamp}</p>
//           <p>₹${challan.amount}</p>
//         </div>
//       `);

//       new tt.Marker()
//         .setLngLat([challan.location.lat, challan.location.lng])
//         .setPopup(popup)
//         .addTo(map);
//     });
//   }, [map, challans]);

//   return (
//     <div className="h-[calc(100vh-2rem)]">
//       <div ref={mapElement} className="w-full h-full" />
//     </div>
//   );
// };

// export default MapView;

import React from "react";
import tt from "@tomtom-international/web-sdk-maps";
import "@tomtom-international/web-sdk-maps/dist/maps.css";
import type { Challan } from "../types";

interface MapViewProps {
  challans: Challan[];
}

const MapView: React.FC<MapViewProps> = ({ challans }) => {
  const mapElement = React.useRef<HTMLDivElement>(null);
  const [map, setMap] = React.useState<tt.Map | null>(null);

  React.useEffect(() => {
    if (!mapElement.current) return;

    const map = tt.map({
      key: "jFf7r7QHWdsF8AFHXCz3Gvbm6kh7uX0j",
      container: mapElement.current,
      center: [72.8777, 19.076],
      zoom: 12,
    });

    setMap(map);

    return () => map.remove();
  }, []);

  React.useEffect(() => {
    if (!map) return;

    challans.forEach((challan) => {
      const popup = new tt.Popup({ offset: 30 }).setHTML(`
        <div class="p-2">
          <h3 class="font-bold">${challan.vehicleNumber}</h3>
          <p>${challan.violation}</p>
          <p>₹${challan.amount}</p>
        </div>
      `);

      new tt.Marker()
        .setLngLat([challan.location.lng, challan.location.lat])
        .setPopup(popup)
        .addTo(map);
    });
  }, [map, challans]);

  return (
    <div className="h-[calc(100vh-2rem)]">
      <div ref={mapElement} className="w-full h-full" />
    </div>
  );
};

export default MapView;
