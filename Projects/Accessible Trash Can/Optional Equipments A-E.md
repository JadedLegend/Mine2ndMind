# **Optional Equipments**

## **Path A — Mostly mechanical**

**Parts:**

- Normal pedal trash can
- Existing pedal linkage
- Added top button/lever
- Cable, rod, latch, spring, brackets
- External button would likely need to be wired or become non-mechanical later

**Pros:**

- Dad-friendly.
- Physical, visible, fixable.
- Good first exploration of the lid mechanics.

**Cons:**

- Hard to make both buttons act as true open/close toggles.
- External stick-on button is not natural in a purely mechanical system.
- Mechanical latch systems can get fiddly.

**Use this path for:** learning the lid geometry, not final behavior.

## **Path B — No-code electric relay system**

**Parts:**

- 12V linear actuator
- 12V power supply
- Wired top momentary button
- Foot pedal microswitch
- Wireless relay/button kit for the external button
- Reversing relay or linear-actuator controller
- Limit switches, ideally built into the actuator

**Pros:**

- No coding.
- More dad-compatible than Arduino if he dislikes electronics.
- Can produce real open/close motion.
- External button can be a simple RF remote / wireless relay.

**Cons:**

- Making **three different buttons all behave as one clean toggle** can get messy with relays.
- Safety timeout, debounce, and state memory are harder without a small controller.
- Debugging relay logic can become more confusing than simple code.

**Use this path for:** a rugged garage prototype if you want to avoid programming completely.

## **Path C — Small controller + actuator**

**Parts:**

- 12V linear actuator with built-in limit switches
- Arduino Nano / Uno or ESP32
- Motor driver or DPDT relay module for polarity reversal
- 12V power supply, likely 3–5A depending on actuator
- Top momentary button
- Foot pedal microswitch
- Wireless external button receiver
- Enclosure, fuse, wire glands, brackets

**Pros:**

- Cleanest match to your actual idea.
- All three inputs can do the exact same thing.
- Easy logic: press any input → toggle open/close.
- Can add timeout protection.
- Can ignore repeated presses while the lid is moving.
- Can later add lights, sound, battery, app, or whatever without rebuilding the whole mechanism.

**Cons:**

- Some coding.
- More abstract for dad unless you present it as a sealed “control box.”
- Needs basic wiring discipline.

**Use this path for:** the best real prototype.

## **Path D — Servo motor**

**Parts:**

- High-torque servo
- Controller
- Buttons
- Power supply
- Bracket/arm linkage

**Pros:**

- Cheap.
- Fast.
- Easy to test on a bench.

**Cons:**

- Full-size trash can lids may overload cheap servos.
- Servos can buzz, strip gears, or fight the lid.
- Less rugged than a linear actuator.
- Holding position may require powered torque unless mechanically latched.

**Use this path for:** tabletop demo only.

## **Path E — Solenoid**

**Parts:**

- Push/pull solenoid
- Relay
- Power supply
- Spring/latch mechanism

**Pros:**

- Simple pulse action.
- Good for releasing a latch.

**Cons:**

- Bad main lid mover. One Adafruit 12V push-pull solenoid lists only **5.5 mm throw** and **0.5 N starting force**, which is far too little for directly moving a kitchen-can lid.

**Use this path for:** latch release only, not lid motion.