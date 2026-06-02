# Crashcourse: DIY Antennas & The Unseen World
*A Workshop Zine for Explorers of Signals and Sounds*

--- PAGE BREAK ---

## The Unseen Sea Around Us

We are surrounded by an invisible ocean of information. Radio stations, weather satellites, Wi-Fi networks, and even Jupiter's storms are constantly broadcasting energy around us. 

An antenna is simply a piece of metal (or wire) that acts as a bridge between that invisible world and our electronic tools. It converts electrical signals into radio waves and back again. When radio waves from a broadcast tower *reach* your antenna, they induce a tiny electrical current in the wire.[^1] Your radio amplifies that current and turns it into sound or data.

Think of it like a tuning fork. A tuning fork only vibrates strongly at one specific pitch. Antennas work the same way: they resonate most powerfully at a specific frequency, determined by their physical length.

## Safety First!

These rules are non-negotiable for builders:

1. **Never run antenna wire near or across power lines.**
2. **Never connect a long wire antenna to a power outlet or any mains-connected device.** The antenna wire can carry lethal induced voltages from lightning or accidental contact with power lines.
3. **Grounding:** Do not use the electrical ground from a power outlet as your radio ground. Use a dedicated copper ground rod driven into damp soil.[^2]
4. **Soldering:** Always work in a well-ventilated area, wear safety glasses, and use lead-free solder when possible.

--- PAGE BREAK ---

## The Magic of Resonance

You can think of radio waves as ripples on a pond. The distance between two ripple crests is the **wavelength**. The number of ripples passing a fixed point per second is the **frequency**. The shorter the wavelength, the higher the frequency.[^3]

### Why Size Matters
An antenna works best when its length matches a resonant fraction of the wavelength—usually half or a quarter of the wave. 

- **AM Radio (530-1,700 kHz):** Wavelengths are huge (176 to 566 meters). A quarter-wave antenna would be up to 141 meters long!
- **FM Radio (88-108 MHz):** Wavelengths are manageable (2.78 to 3.41 meters).
- **Wi-Fi (2.4 GHz):** Wavelengths are tiny (12.5 cm).

### The Master Formula
All antenna size calculations begin with one formula:
`Wavelength (meters) = 300 / Frequency (MHz)`

For a **Half-Wave Dipole**, the total length in meters is:
`142.65 / Frequency (MHz)`

For a **Quarter-Wave Monopole**, the length in meters is:
`75 / Frequency (MHz)`

*(Always cut your wire slightly long, then trim it down for the best reception!)*

--- PAGE BREAK ---

## Workshop Part 1: The Scavenger Hunt

Before we build, we need materials. You don't need to buy expensive parts to start exploring the radio spectrum!

### Finding Wire
You need wire for coils and antennas. Before buying any:
- **Dead electric motors** (fans, appliances): Unwind the coils for enameled wire.
- **Ethernet cable (Cat5/Cat6):** Four twisted pairs of solid AWG 24 copper wire. A patch cable gives you 3–15 feet of wire; bulk spools give 50+ feet. Either is useful for coil-winding.
- **Old extension cords or lamp cord:** Stranded copper, perfect for stringing up long antennas.

### Listening to the Spectrum
If you have an **RTL-SDR** (a $20 USB dongle), you can plug it into any laptop and instantly see the radio spectrum from 24 MHz to 1.7 GHz.[^4] 
- To start exploring, all you need is a simple quarter-wave wire plugged into the SDR. 
- **For FM Radio:** Use a 76 cm wire (about 30 inches).
- **For Wi-Fi:** Use a 3.1 cm wire. 

--- PAGE BREAK ---

## Workshop Part 2: Catching FM (The Dipole)

The **T-Dipole** is the standard indoor FM antenna. It performs much better than a wire draped randomly over furniture. 

**Materials:**
- 1.6 meters (~5.5 feet) of two-conductor wire (speaker wire or lamp cord)
- Wire strippers & Tape

**The Math (For 98 MHz FM Center):**
Using our formula: `142.65 / 98 = 1.456 meters total`.
The practical range for the FM band is **132 to 162 cm** total length.[^5] A 150 cm total length (75 cm per arm) is a great starting point.

**How to Build:**
1. Cut your wire to 160 cm. At the exact midpoint (80 cm), separate the two conductors for about 3 cm. Do NOT cut them, just peel them apart.
2. Strip both conductors at the midpoint, exposing 1 cm of bare wire on each side. These are your feed points.
3. From the midpoint, extend each conductor outward (one left, one right) for 75 cm. At the ends, strip 1 cm and fold the bare wire back on itself.
4. The remaining wire going down is your "feedline" to your radio. Connect the stripped midpoint wires to your radio's FM antenna terminals. 
5. *(Note: If your radio has a 75 Ohm coaxial input, you'll need a 300-to-75 Ohm matching transformer (a 'balun'). Plug the twin-lead wires into the balun's 300 Ohm terminals, then run a coax cable from its 75 Ohm port to the radio).*[^6]
6. Mount the T-shape horizontally on a wall. Horizontal mounting matches the polarization of most FM stations. In the worst case, a polarization mismatch can cost you 20 dB of signal—meaning your radio receives 100 times less power than it could. While many FM stations now broadcast a mixed signal so the loss is smaller, it's still worth matching polarization when you can.

--- PAGE BREAK ---

## Workshop Part 3: AM & The Foxhole Radio

AM radio waves are enormous, so we use coils (inductors) to catch them magnetically. The **Foxhole Radio** is the ultimate low-cost AM receiver, built from trash by WWII soldiers. It requires NO batteries!

**Materials:**
- 1 cardboard tube (toilet paper roll)
- ~15 meters of thin wire (salvaged)
- 1 razor blade (blue or rusty works best)
- 1 pencil stub (wood, not mechanical)
- 1 safety pin & 2 thumbtacks
- 1 high-impedance earphone (piezo buzzer salvaged from a greeting card)

**How to Build:**
1. Wind 100-120 turns of wire tightly around the cardboard tube.
2. Tack the razor blade flat onto a wood base using a thumbtack. 
3. Break the pencil to expose ~1 cm of graphite. Tape the pencil to the safety pin.
4. Mount the safety pin on a second thumbtack so the graphite tip rests lightly on the razor blade.
5. **Connections:** 
   - Antenna wire (long wire out a window) to one end of the coil.
   - Other end of coil to the razor blade (via thumbtack).
   - Safety pin (pencil side) to one earphone wire.
   - Other earphone wire to ground (metal pipe or earth stake).

**Why it works:** 
The thin oxide layer on the razor blade surface acts as a semiconductor junction. The graphite pencil lead makes point contact with this layer, creating a crude diode that demodulates AM signals, turning radio waves directly into audio you can hear!

*(If you want to upgrade, use a 1N34A Germanium Diode and a Variable Capacitor to make a true Crystal Radio).*[^7]

--- PAGE BREAK ---

## Workshop Part 4: Exploring the Unknown 

For Wi-Fi and microwaves, wavelengths are tiny. You can build highly directional antennas from everyday objects.

### The Cantenna (Wi-Fi Booster)
A cylindrical metal can acts as a *waveguide*—a funnel that forces 2.4 GHz signals to travel in one direction while blocking them from spreading sideways. The closed back reflects them out the open front.

**Materials:**
- 1 solid metal can (diameter ~92 mm / 3.6 inches)
- N-type or RP-SMA connector & short copper wire

**How to Build:**
1. Drill a hole **59.8 mm** from the closed bottom of the can. *(This position is empirically optimized for a 92 mm can at 2.4 GHz. The exact optimal depth shifts slightly depending on can diameter).*[^8]
2. Cut a copper probe wire to exactly **30.9 mm**. Solder it to your connector.
3. Insert the connector into the hole so the probe sits inside the can. Connect to your Wi-Fi device. 

### The Yagi-Uda
The classic rooftop antenna. It uses multiple elements to "steer" the beam forward. 
For 2.4 GHz Wi-Fi, you can build a 5-element Yagi out of straightened paper clips and a popsicle stick![^9] 
- Driven element: 5.91 cm
- Reflector: 6.19 cm (placed 1.56 cm behind driven)
- Directors: 5.50 cm, 5.22 cm, 5.00 cm (spaced in front)

--- PAGE BREAK ---

## Making Your Own Components

### Homemade Variable Capacitor
A variable capacitor is used to tune your radio to specific stations.

**Materials:** 
Cardboard, aluminum foil, plastic page protectors, and a machine screw.

**How to Build:**
1. **Stator (fixed plate):** Glue foil onto cardboard (15 cm circle). Cover with a plastic protector. Attach a wire.
2. **Rotor (moving plate):** Glue foil to a cardboard half-circle (14 cm). Cover with plastic. Attach a wire.
3. Stack the rotor on top of the stator with the screw as a pivot.
4. The capacitance depends on plate overlap area and dielectric thickness. Larger plates = more capacitance. Thicker dielectric = less capacitance. With thin plastic sheet (page protector), expect roughly 2–4 pF per cm² of overlap area. A 15 cm half-circle (88 cm²) would produce approximately **175–350 pF**. The exact range will vary — tune empirically![^10]

### Experimental Listening & Aesthetics
Antennas aren't just for perfect reception—they are aesthetic and experimental tools. Try building large, sculptural loop antennas, or using inductive coupling (holding a coil near a device) to listen to the "hidden songs" of your electronics. EMF listening reveals the rhythmic pulses of our modern world.

--- PAGE BREAK ---

## References & Resources

1. **How Antennas Work:** When radio waves reach an antenna, they induce a current. [OmniCalculator Dipole](https://www.omnicalculator.com/physics/dipole)
2. **Safety Guidelines:** [OpenLearn Crystal Radio Safety](https://www.open.edu/openlearn/science-maths-technology/science/physics-and-astronomy/physics/building-crystal-radio-set)
3. **Wavelengths & Frequencies:** [Antenna Quarter Wave Calculator](https://wavelength-calculator.com/antenna-quarter-wave-calculator.php)
4. **SDR Resources:** [Luke Attubato Making My Own Antennas](https://lukeattubato.com/making-my-own-antennas)
5. **FM Dipole Construction:** [Electronics Notes FM Dipole](https://www.electronics-notes.com/articles/antennas-propagation/dipole-antenna/fm-dipole-antenna.php)
6. **Baluns and Transformers:** [Radio4All 75 Ohm FM Antenna](https://www.radio4all.org/how-to-make-a-75-ohm-fm-antenna/)
7. **Crystal Radios & AM Loops:** [4mcveys.net AM Loop](https://www.4mcveys.net/2018/10/05/a-very-efficient-loop-antenna-for-am-broadcasts/), [Techlib Crystal Radio Circuits](https://www.techlib.com/electronics/crystal.html)
8. **Cantenna Waveguides:** [wikarekare.org Waveguide Can Calculator](http://www.wikarekare.org/Antenna/WaveguideCan.html)
9. **Yagi Design:** [RF Wireless World Yagi Calculator](https://www.rfwireless-world.com/calculators/3-element-yagi-antenna-calculator)
10. **Homemade Capacitors:** Based on practical air/plastic-gap models.

*This zine is open-source. Share, copy, and explore the signals around you!*
