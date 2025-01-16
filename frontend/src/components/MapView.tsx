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
      key: "DOI22fw3rak3ZpE2sbgAvECqH1GgxWWr",
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
