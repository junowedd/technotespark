# IR drop 45mV > 40mV
db_enhance_metal -net VDD -coord 120.5 450.2 -add_width 0.2

# IR drop 85mV > 40mV
db_enhance_metal -net VDD -coord 500.0 500.0 -add_width 0.2

# Single Via Reliability
db_insert_via -net SIGNAL_A -coord 150.2 300.5 -type DOUBLE

