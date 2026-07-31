stateDiagram-v2
    direction LR

    [*] --> Scheduled

    Scheduled --> CheckedIn : Check-in
    Scheduled --> Cancelled : Patient cancels
    Scheduled --> NoShow : No show

    CheckedIn --> InProgress : Start consultation
    CheckedIn --> Cancelled : Cancel

    InProgress --> Completed : Complete

    Completed --> [*]
    Cancelled --> [*]
    NoShow --> [*]

    classDef default fill:#ffffff,stroke:#64748b,color:#0f172a
    classDef start fill:#eff6ff,stroke:#2563eb
    classDef success fill:#f0fdf4,stroke:#16a34a
    classDef end fill:#f8fafc,stroke:#94a3b8

    class Scheduled start
    class Completed success
    class Cancelled,NoShow end