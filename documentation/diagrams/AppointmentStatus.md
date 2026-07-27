stateDiagram-v2
    [*] --> scheduled

    scheduled --> cancelled : Patient cancel
    scheduled --> checked_in : Doctor/Admin check-in
    scheduled --> no_show : Doctor/Admin no show

    checked_in --> in_progress : Doctor/Admin start consultation
    checked_in --> cancelled : Doctor/Admin cancel

    in_progress --> completed : Doctor/Admin complete

    completed --> [*]
    cancelled --> [*]
    no_show --> [*]