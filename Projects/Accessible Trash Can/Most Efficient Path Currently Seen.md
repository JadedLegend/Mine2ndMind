# **Most Efficient Path Currently Seen**

## **Recommended build: electric foot switch + top button + external wireless button + 12V linear actuator + small controller**

Not WiFi.  
Not app.  
Not motion sensor.  
Not voice.  
Not “smart home.”

Just a small controller reading three buttons.

Foot pedal switch

Top button

External wireless button

↓

Small controller

↓

Motor driver / reversing relay

↓

12V linear actuator

↓

Lid opens or closes

## **Why this is the best route**

It matches the idea exactly:

- Foot pedal: one control.
- Top button: press once open, press again close.
- External button: press once open, press again close.

It avoids the biggest failure mode: trying to force a normal mechanical pedal can to become a perfect toggle system.

A linear actuator is better than a solenoid because it has real travel and force. Pololu’s actuator listings show small micro actuators around **30 mm stroke, 22 N / 4.9 lb dynamic load, 28 mm/s no-load speed**, with built-in limit switches and IP66 rating. Larger 12V actuators can be much stronger; one 4-inch Pololu model lists **110 lb load rating**, **0.6 in/s max speed**, built-in limit switches, and a worm drive that holds position unpowered.

The tradeoff is speed. A strong 4-inch actuator at 0.6 in/s could take several seconds to fully travel. So the best practical choice is probably **not the strongest actuator**. It is the shortest-stroke actuator that can move the lid reliably.

## **My recommended prototype order**

### **Prototype 0 — mechanism only**

Buy or use a pedal trash can.

Do not modify electronics yet.

Measure:

- Where the lid naturally wants to open from.
- How much travel the lid needs.
- Whether the lid can be opened from the back hinge area.
- Whether the lid can be closed by pulling down or retracting.
- How much force is needed.

Simple test: use a fish scale/luggage scale and pull the lid or linkage until it moves.

### **Prototype 1 — wired electric version**

Build with:

- 12V actuator
- Top button
- Foot pedal switch
- Controller
- Power supply

Skip the external wireless button for the first bench test. Use a third wired button to simulate it.

Goal:

Any button toggles the lid.

### **Prototype 2 — add external button**

Add:

- 433 MHz wireless button/receiver, or
- simple wireless relay receiver

The external button should feed the same input as the wired buttons.

### **Prototype 3 — clean enclosure**

Add:

- sealed electronics box
- strain relief
- fuse
- manual power switch
- hidden wiring
- bracket cleanup
- maybe a manual emergency release

## **Controller logic**

The code is small:

State = CLOSED

When any button is pressed:

If lid is moving:

ignore press

If State is CLOSED:

drive actuator open

State = OPEN

Else if State is OPEN:

drive actuator closed

State = CLOSED

Add safety:

If actuator runs longer than expected:

stop motor

That prevents the motor from grinding if something jams.

## **Parts \*direction\*  
Not final shopping list**

For the first real prototype, look for:

- **12V linear actuator, 2 inch stroke, built-in limit switches**
- **Arduino Nano or Arduino Uno**
- **12V DC motor reversing relay module** or **BTS7960 motor driver**
- **momentary waterproof push button, normally open**
- **microswitch foot pedal switch**
- **433 MHz wireless momentary receiver and button**
- **12V 3A or 5A power supply**
- **inline fuse holder**
- **small plastic project box**
- **metal brackets / aluminum flat bar**

A higher-end actuator path could use something like Progressive Automations’ feedback actuator line, which lists 12V options with 2-inch stroke and 35 lb / 150 lb force choices, but those are more expensive—around **$152.99** at the checked listing.