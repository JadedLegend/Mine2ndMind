The core architecture

The trashcan needs four subsystems:

\`\`\`text

1\. Lid + hinge

2\. Foot pedal mechanism

3\. Motorized opener/closer

4\. Button system: lid button + wireless remote

\`\`\`

The key engineering question is:

\> How does the motor open the lid without fighting the foot pedal?

That’s the center of the build.

\---

Route 1: Servo-motor prototype

This is the simplest first prototype.

Parts

Existing foot-pedal trash can

Arduino Nano / Uno / ESP32

High-torque servo motor

Push button for lid

Wireless relay kit or RF button receiver

Battery pack or USB power bank

Wires

Mounting bracket

Servo arm linkage to lid

Arduino’s own smart trash can example uses a servo to move a lid, and many beginner smart-bin builds use the same basic pattern: microcontroller + sensor/input + servo + lid attachment. (\[Arduino\]\[1\])

How it works

The servo rotates between two angles:

\`\`\`text

0° = lid closed

80° = lid open

\`\`\`

Button press tells the controller:

\`\`\`text

If closed → open

If open → close

\`\`\`

Pros

Cheapest route

Easiest to understand

Good for proving the user experience

Uses common hobby parts

Easy to revise

Cons

Servo may be too weak for larger lids

Can buzz or strain if the lid resists

Mounting geometry matters a lot

Foot pedal conflict needs careful handling

Best use

First working demo.

This is the “make the idea breathe” version.

\---

Route 2: Linear actuator prototype

This is stronger and more product-like mechanically.

Parts

Foot-pedal trash can

Small 12V linear actuator

Motor driver / relay module

Microcontroller

Lid button

Wireless remote receiver

12V battery pack

Mounting brackets

Limit switches, ideally

Linear actuators are commonly used for opening/closing lids, panels, and boxes with Arduino-style controllers. They are stronger than servos but require more careful mounting because a lid rotates while the actuator pushes in a straight line. (\[Instructables\]\[2\])

How it works

The actuator extends to open the lid.

It retracts to close the lid.

\`\`\`text

Actuator short = closed

Actuator long = open

\`\`\`

Pros

Stronger

More reliable for heavier lids

More “appliance-like”

Can hold lid open firmly

Cons

More expensive

Slower

Noisier

Requires 12V power

More mechanical planning

Best use

Second-stage prototype after the servo version proves the concept.

This is the “make it sturdy” version.

\---

Route 3: Motorized hinge route

This is the cleanest eventual product route.

Parts

Custom hinge

Gear motor or torque motor

Encoder or limit switches

Control board

Button inputs

Wireless receiver

Rechargeable battery

Custom lid assembly

How it works

Instead of pushing the lid from the outside, the hinge itself becomes powered.

The motor lives at the hinge and rotates the lid directly.

Pros

Cleanest design

Hidden mechanism

Best consumer-product feel

Easier to enclose safely

Less ugly linkage

Cons

Hardest to prototype

Requires custom mechanical design

More expensive

Needs stronger engineering support

Best use

Final product development.

This is the “make it elegant” version.

\---

Route 4: Modify an existing motion-sensor trash can

This may be the fastest hack.

Parts

Existing automatic trash can

Its built-in motor/lid system

Added lid button

Added wireless remote trigger

Possibly bypass or replace motion sensor circuit

How it works

Instead of building the lid motor system from scratch, you use the existing automatic can’s motor and board.

Then you add your preferred controls:

\`\`\`text

Top button → trigger open/close

Wireless button → trigger open/close

\`\`\`

Pros

Fastest path to a demo

Motor and lid geometry already solved

Looks more finished immediately

Less physical fabrication

Cons

Harder to understand the existing electronics

Cheap models may be poorly documented

Risk of breaking the board

Less control over behavior

Best use

A convincing proof-of-concept video.

This is the “borrow the skeleton” version.

\---

Remote button options

Option A: Wireless relay kit

A wireless relay receiver lives inside the trashcan.

The adhesive remote sends it a signal.

The relay acts like a button press.

This is probably your best path. 433 MHz remote relay kits are common off-the-shelf parts. (\[QIACHIP\]\[3\])

Pros

Simple

Cheap

No custom wireless coding

Remote can be adhesive-backed

Cons

May be bulky

Range/quality varies

Some modules need configuration

\---

Option B: Bluetooth remote

Use ESP32 and a Bluetooth button.

Pros

Modern

App-expandable later

Cleaner long-term

Cons

More coding

Pairing can be annoying

More power drain

\---

Option C: Hardwired button first

Before wireless, use a second wired button.

Pros

Best learning step

Proves the logic

Removes wireless complexity

Cons

Not the final experience

This is what I’d do first.

\---

The part list I’d start with

For the first real prototype:

\`\`\`text

Trashcan:

\- Medium foot-pedal trash can with light plastic lid

Brain:

\- Arduino Nano or ESP32

Motion:

\- High-torque servo motor

\- Servo horn/arm

\- Metal linkage rod or stiff wire

Inputs:

\- Momentary push button for lid

\- Wireless relay receiver + adhesive remote

Power:

\- 5V USB power bank for servo version

\- Separate 5V supply if servo draws too much current

Safety/feedback:

\- Optional limit switch for lid open

\- Optional limit switch for lid closed

Mechanical:

\- Small L-brackets

\- Screws/bolts

\- Epoxy or 3M VHB tape

\- Cable clips

\- Small enclosure for electronics

\`\`\`

For the servo, don’t start with a tiny SG90 unless the lid is very light. You’ll likely want something in the MG996R / DS3218-ish family, because torque matters. Servo torque is basically: how much twisting strength the motor has at a certain distance from the hinge. Larger lids need more torque. (\[kpower.com\]\[4\])

\---

The cleanest build sequence

Phase 1: Button opens lid

No remote. No foot-pedal integration concern yet.

\`\`\`text

Button → controller → servo → lid opens/closes

\`\`\`

Phase 2: Preserve foot pedal

Adjust the linkage so the foot pedal can still open the lid without forcing the motor.

This may require a loose joint, spring, or slotted connector.

Phase 3: Add wireless button

\`\`\`text

Wireless button → receiver → same input as lid button

\`\`\`

The remote should not be a separate “brain.”

It should simply imitate the button.

Phase 4: Make it graceful

Add:

slower lid movement

quiet close

hidden wires

better housing

rechargeable power

clean button placement

\---

Biggest design risks

1\. Motor fighting the pedal

This is the main one.

Solution direction: make the motor linkage tolerant, not rigid.

Think:

\`\`\`text

Foot pedal = original body movement

Motor = assisting hand

\`\`\`

They should both be able to move the lid without damaging each other.

2\. Lid weight

A heavy lid makes everything harder.

Start with a lightweight lid.

3\. Battery life

A servo can draw real current when moving or holding position.

Later, the system should cut motor power after reaching open/closed state.

4\. Cheap wireless modules

They work, but documentation can be cryptic.

That’s why I’d prototype with a wired second button first, then replace that button with wireless.

\---

My recommendation

Start here:

\> Route 1, but with Route 4 as a backup.

Meaning:

First try to build the mechanism yourself using a light foot-pedal can, Arduino/ESP32, and high-torque servo.

But also keep an existing automatic trashcan nearby as a possible donor body if the hinge geometry becomes annoying.

The first prototype does not need to be beautiful. It needs to prove this sentence:

\> “A trashcan with foot, lid-button, and remote-button access feels obviously better once used.”

That’s the actual invention. The mechanism is just the doorway.