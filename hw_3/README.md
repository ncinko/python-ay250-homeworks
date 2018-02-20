hw_3 README

Problem 1:

instructions for my_credentials.py (how to use API services, e-mail, etc.)

Problem 2:

Code solution: hw3_problem2.py  As written, a 'sound_files' directory is assumed to be in the same directory as the script; it runs over all .aif files in 'sound_files'.
power_spectrum.png contains an example frequency power spectrum obtained from a FFT.  We see the fundamental frequency at ~175 Hz (F3) and the next overtone at ~350 Hz.
It seems to get the notes pretty well; 5.aif is a bit weird to me because the G2 is really dominant by ear, but the power spectrum shows a ~147 Hz (D3) signal.  Also, I hear
an octave in 2.aif, so I added the amplitude comparison criterion--but this showed the higher power F5 frequency in F4_CathedralOrgan.aif.  I'm not sure how to handle both
these cases simultaneously given the results of the FFT.

Text output from program (I re-ordered the output):

Notes found in 1.aif:
C4
D4
G4
=====================
Notes found in 2.aif:
F3
F4
=====================
Notes found in 3.aif:
A4
=====================
Notes found in 4.aif:
C4
=====================
Notes found in 5.aif:
G2
D3
=====================
Notes found in 6.aif:
C5
=====================
Notes found in 7.aif:
D5
=====================
Notes found in 8.aif:
F4
=====================
Notes found in 9.aif:
G3
=====================
Notes found in 10.aif:
C2
=====================
Notes found in 11.aif:
E2
=====================
Notes found in 12.aif:
C2
=====================
Notes found in A4_PopOrgan.aif:
A4
=====================
Notes found in C4+A4_PopOrgan.aif:
C4
A4
=====================
Notes found in F3_PopOrgan.aif:
F3
=====================
Notes found in F4_CathedralOrgan.aif:
F4
F5
=====================