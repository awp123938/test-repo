import math
import argparse


def simulate_trajectory(v0, angle_deg, bc, distance, dt=0.001, g=9.80665):
    angle = math.radians(angle_deg)
    vx = v0 * math.cos(angle)
    vy = v0 * math.sin(angle)
    x, y = 0.0, 0.0
    # Atmospheric density at sea level (kg/m^3)
    rho = 1.225
    k = 0.5 * rho / bc
    t = 0.0

    while x < distance and y >= 0:
        v = math.hypot(vx, vy)
        ax = -k * v * vx
        ay = -g - k * v * vy
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        t += dt
    return {
        "time": t,
        "drop": -y,
        "final_velocity": math.hypot(vx, vy)
    }


def main():
    parser = argparse.ArgumentParser(description="Simple ballistic calculator")
    parser.add_argument("velocity", type=float, help="Muzzle velocity (m/s)")
    parser.add_argument("angle", type=float, help="Angle of departure (degrees)")
    parser.add_argument("bc", type=float, help="Ballistic coefficient")
    parser.add_argument("distance", type=float, help="Target distance (m)")
    parser.add_argument("--dt", type=float, default=0.001, help="Time step (s)")
    args = parser.parse_args()

    result = simulate_trajectory(args.velocity, args.angle, args.bc, args.distance, args.dt)

    print(f"Time of flight: {result['time']:.3f} s")
    print(f"Drop at {args.distance} m: {result['drop']:.3f} m")
    print(f"Velocity at target: {result['final_velocity']:.3f} m/s")


if __name__ == "__main__":
    main()
