import React from "react";
import tt from "@tomtom-international/web-sdk-maps";
import "@tomtom-international/web-sdk-maps/dist/maps.css";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  BarChart,
  XAxis,
  YAxis,
  Bar,
  Tooltip,
  LineChart,
  Line,
} from "recharts";
import type { Challan } from "../types";

interface MapViewProps {
  challans: Challan[];
}

const MapView: React.FC<MapViewProps> = ({ challans }) => {
  const mapElement = React.useRef<HTMLDivElement>(null);
  const [map, setMap] = React.useState<tt.Map | null>(null);

  // Analytics calculations
  const totalAmount = challans.reduce(
    (sum, challan) => sum + challan.amount,
    0
  );
  const avgAmount = totalAmount / challans.length || 0;

  // Group violations by type
  const violationStats = React.useMemo(() => {
    const stats = challans.reduce((acc, challan) => {
      acc[challan.violation] = (acc[challan.violation] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return Object.entries(stats).map(([violation, count]) => ({
      violation,
      count,
    }));
  }, [challans]);

  // Group by hour of day for time analysis
  const timeAnalysis = React.useMemo(() => {
    const hourCounts = new Array(24).fill(0);
    challans.forEach((challan) => {
      const hour = new Date(challan.time_stamp).getHours();
      hourCounts[hour]++;
    });
    return hourCounts.map((count, hour) => ({
      hour: `${hour}:00`,
      incidents: count,
    }));
  }, [challans]);

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
    <div className="p-4 space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <Card>
          <CardHeader>
            <CardTitle>Total Challans</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{challans.length}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Total Amount</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">
              ₹{totalAmount.toLocaleString()}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Average Fine</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">₹{avgAmount.toLocaleString()}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <Card>
          <CardHeader>
            <CardTitle>Violations by Type</CardTitle>
          </CardHeader>
          <CardContent>
            <BarChart width={400} height={300} data={violationStats}>
              <XAxis dataKey="violation" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Incidents by Hour</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChart width={400} height={300} data={timeAnalysis}>
              <XAxis dataKey="hour" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="incidents" stroke="#82ca9d" />
            </LineChart>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Incident Map</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[calc(100vh-36rem)]">
            <div ref={mapElement} className="w-full h-full" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MapView;
