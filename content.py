# -*- coding: utf-8 -*-
"""
NextMind Learning website - configuration and content.
Everything shown on the site comes from this file.
Edit CONFIG, then run:  python3 build.py
"""

CONFIG = {
    # REQUIRED - full address where the site will live, no trailing slash.
    # Custom domain: "https://www.nextmindlearning.com"
    # GitHub project page: "https://USERNAME.github.io/REPO"
    "site_url": "https://nextmindlearning.com",

    # REQUIRED - public contact email shown on the site.
    "email": "info@nextmindlearning.com",

    # REQUIRED for the contact form - create a free form at formspree.io
    # and paste its endpoint here.
    "form_endpoint": "https://formspree.io/f/mqpeojjd",

    # OPTIONAL - leave empty ("") to hide.
    "phone": "",
    "linkedin": "",

    # OPTIONAL - only if you use a custom domain (writes the CNAME file).
    "custom_domain": "nextmindlearning.com",

    "brand": "NextMind Learning",
}

# ---------------------------------------------------------------- routes
ROUTES = {
    "home":     {"es": "",                         "en": "en/"},
    "courses":  {"es": "cursos-para-empresas/",    "en": "en/corporate-courses/"},
    "partners": {"es": "alianzas-universitarias/", "en": "en/university-partnerships/"},
    "camps":    {"es": "campamentos/",             "en": "en/camps/"},
    "about":    {"es": "sobre-nosotros/",          "en": "en/about/"},
    "contact":  {"es": "contacto/",                "en": "en/contact/"},
}

NAV = ["courses", "partners", "camps", "about"]

UI = {
    "es": {
        "nav": {"home": "Inicio", "courses": "Cursos para empresas", "partners": "Alianzas universitarias",
                "camps": "Campamentos", "about": "Sobre nosotros", "contact": "Contacto"},
        "cta": "Contáctanos",
        "skip": "Saltar al contenido",
        "menu": "Menú",
        "switch": "English",
        "switch_lang": "en",
        "footer_tag": "Formación ejecutiva en inteligencia artificial y tecnología para grandes empresas, con profesorado de universidades de referencia mundial.",
        "footer_nav": "Navegación",
        "footer_contact": "Contacto",
        "rights": "Todos los derechos reservados.",
        "universities_note": "Fotografías: Unsplash. Vídeo: Mixkit.",
    },
    "en": {
        "nav": {"home": "Home", "courses": "Corporate courses", "partners": "University partnerships",
                "camps": "Camps", "about": "About us", "contact": "Contact"},
        "cta": "Contact us",
        "skip": "Skip to content",
        "menu": "Menu",
        "switch": "Español",
        "switch_lang": "es",
        "footer_tag": "Executive education in artificial intelligence and technology for large companies, with faculty from world-leading universities.",
        "footer_nav": "Navigation",
        "footer_contact": "Contact",
        "rights": "All rights reserved.",
        "universities_note": "Photos: Unsplash. Video: Mixkit.",
    },
}

# ---------------------------------------------------------------- shared blocks
FORMATS = {
    "es": [
        ("Programas predefinidos",
         "Cursos online de catálogo de universidades de referencia mundial, listos para lanzar. Según el programa, superar las evaluaciones o un proyecto final da acceso al certificado de la institución."),
        ("Programas blended",
         "Módulos online combinados con talleres interactivos con profesorado universitario, para llevar lo aprendido a la práctica más rápido."),
        ("Programas virtuales en directo",
         "Sesiones virtuales en directo adaptadas a su audiencia, su sector y su contexto: desde una sesión ejecutiva o una masterclass hasta itinerarios de varias sesiones."),
        ("Programas a medida",
         "Currículos creados junto a su organización para cubrir carencias concretas en tecnología, innovación y liderazgo. Online o presenciales, como iniciativa independiente o junto a servicios de asesoramiento, desde talleres intensivos hasta academias de largo plazo."),
        ("Consultoría ejecutiva",
         "Acompañamiento en estrategia de aprendizaje, desarrollo de capacidades y alineación de la formación ejecutiva con los objetivos de transformación del negocio."),
    ],
    "en": [
        ("Pre-designed programs",
         "Ready-to-launch online courses from world-leading universities. Depending on the program, completing the assessments or a capstone project leads to the institution's certificate."),
        ("Blended programs",
         "Online modules combined with interactive workshops led by university faculty, so participants apply what they learn sooner."),
        ("Live virtual programs",
         "Live online sessions tailored to your audience, industry and context: from a single executive session or masterclass to multi-session learning journeys."),
        ("Custom programs",
         "Curricula built with your organization to close specific technology, innovation and leadership gaps. Online or in person, standalone or combined with advisory support, from short intensive workshops to long-term academies."),
        ("Executive consulting",
         "Guidance on learning strategy, capability building and aligning executive education with your business transformation goals."),
    ],
}

PROCESS = {
    "es": [
        ("Primera conversación", "Nos cuenta qué quiere conseguir. Antes de compartir contenidos sensibles, firmamos un acuerdo de confidencialidad."),
        ("Diagnóstico", "Le ayudamos a identificar qué necesita aprender cada nivel de la organización, conectando la visión de la dirección con las necesidades reales de los equipos técnicos."),
        ("Propuesta a medida", "Le presentamos una propuesta concreta: audiencia, formato, duración y certificación."),
        ("Diseño con el profesorado", "Desarrollamos el contenido directamente con el profesorado universitario, a partir de los retos de su empresa."),
        ("Impartición y evaluación", "Impartimos el programa y medimos el aprendizaje con evaluaciones previas y posteriores, con recomendaciones para los siguientes pasos."),
        ("Escalado", "Un programa que funciona puede ampliarse a otros departamentos, filiales y países."),
    ],
    "en": [
        ("First conversation", "You tell us what you want to achieve. Before any sensitive material is shared, we sign a confidentiality agreement."),
        ("Needs assessment", "We help you pin down what each level of the organization needs to learn, connecting leadership's vision with the real needs of technical teams."),
        ("Tailored proposal", "We present a concrete proposal: audience, format, duration and certification."),
        ("Design with faculty", "We build the content directly with university faculty, starting from your company's challenges."),
        ("Delivery and assessment", "We deliver the program and measure learning with pre- and post-program assessments, plus recommendations for next steps."),
        ("Scale", "A program that works can be extended to other departments, subsidiaries and countries."),
    ],
}

AUDIENCE = {
    "es": ["Consejeros delegados y comités de dirección", "Alta dirección", "Directores y responsables de departamento",
           "Líderes técnicos y responsables de ingeniería", "Talento de alto potencial",
           "Equipos de innovación, transformación digital y estrategia"],
    "en": ["CEOs and executive committees", "Senior leadership teams", "Directors and heads of department",
           "Technical leaders and engineering managers", "High-potential talent",
           "Innovation, digital transformation and strategy teams"],
}

OUTCOMES = {
    "es": ["Acelerar la adopción de la inteligencia artificial y la transformación digital.",
           "Dar a la dirección criterio propio en IA, ciberseguridad, computación cuántica e ingeniería avanzada.",
           "Tomar mejores decisiones de inversión tecnológica e innovación.",
           "Reforzar la cultura de ciberseguridad y la resiliencia de la organización.",
           "Usar los datos y la analítica para decidir.",
           "Diseñar, liderar y escalar productos y servicios tecnológicos.",
           "Formar líderes capaces de gestionar la complejidad y el cambio.",
           "Integrar la sostenibilidad, el buen gobierno y la innovación responsable en la estrategia."],
    "en": ["Accelerate AI adoption and digital transformation.",
           "Give leadership real fluency in AI, cybersecurity, quantum computing and advanced engineering.",
           "Make better technology investment and innovation decisions.",
           "Strengthen cybersecurity awareness and organizational resilience.",
           "Use data and analytics to drive decisions.",
           "Design, lead and scale technology-driven products and services.",
           "Develop leaders who can navigate complexity and change.",
           "Build sustainability, governance and responsible innovation into long-term strategy."],
}

FAQ_HOME = {
    "es": [
        ('¿Con qué universidades trabajan?',
         'Trabajamos con el instituto tecnológico de referencia mundial con sede en Cambridge, Massachusetts, incluida su formación profesional online y presencial, y con la universidad más antigua de Estados Unidos, en la misma ciudad. También colaboramos con una universidad de investigación de Baltimore de referencia en salud pública y con una gran universidad pública de Seattle. Compartimos el nombre de cada institución en nuestras propuestas.'),
        ("¿Los participantes reciben un certificado?",
         "Algunos programas incluyen un certificado expedido por la institución correspondiente, sujeto a sus requisitos, como completar evaluaciones o un proyecto final. En cada propuesta indicamos si el programa es certificado."),
        ("¿Los cursos son online o presenciales?",
         "Ambas cosas. El profesorado puede impartir sesiones en remoto, viajar a su país para sesiones presenciales o recibir a grupos seleccionados en el campus."),
        ("¿Para cuántas personas se diseñan los programas?",
         "Desde grupos reducidos de alta dirección hasta programas para cientos de mandos y profesionales técnicos."),
        ("¿Cuánto cuesta un programa?",
         "Cada programa se presupuesta según su alcance: audiencia, formato, duración y certificación. Cuéntenos su proyecto y le prepararemos una propuesta."),
        ("¿En qué países trabajan?",
         "Trabajamos con organizaciones en España y Latinoamérica, y los programas pueden desplegarse en otros países."),
    ],
    "en": [
        ('Which universities do you work with?',
         'We work with the world-leading institute of technology based in Cambridge, Massachusetts, including its online and in-person professional education, and with the oldest university in the United States, in the same city. We also work with a Baltimore research university known for public health and with a major public university in Seattle. We share each institution’s name in our proposals.'),
        ("Do participants receive a certificate?",
         "Selected programs include a certificate issued by the corresponding institution, subject to its requirements, such as completing assessments or a capstone project. Every proposal states whether the program is certified."),
        ("Are the courses online or in person?",
         "Both. Faculty can teach remotely, travel to your country for on-site sessions, or host selected cohorts on campus."),
        ("How many people can a program serve?",
         "From small executive cohorts to programs for hundreds of managers and technical professionals."),
        ("How much does a program cost?",
         "Each program is quoted according to its scope: audience, format, duration and certification. Tell us about your project and we will prepare a proposal."),
        ("Where do you work?",
         "We work with organizations in Spain and Latin America, and programs can be rolled out in other countries."),
    ],
}

FAQ_COURSES_EXTRA = {
    "es": [
        ("¿Pueden diseñar un programa exclusivo para nuestra empresa?",
         "Sí. Un currículo diseñado específicamente para su organización puede desplegarse después en sus filiales y en otros países."),
        ('¿Se pueden combinar dos universidades en un mismo programa?',
         'Sí. Un programa puede combinar contenido técnico del instituto tecnológico de Cambridge, Massachusetts, con contenido de liderazgo de la universidad más antigua de Estados Unidos. Cuando hay certificación, cada institución certifica su parte.'),
        ('¿Los cursos online son de la propia universidad?',
         'Sí. Los programas predefinidos y blended utilizan cursos de la plataforma de formación profesional online de la universidad, y sus certificados los expide la propia institución.'),
    ],
    "en": [
        ("Can you design an exclusive program for our company?",
         "Yes. A curriculum designed specifically for your organization can later be rolled out across your subsidiaries and in other countries."),
        ('Can two universities be combined in one program?',
         'Yes. A program can combine technical content from the institute of technology in Cambridge, Massachusetts with leadership content from the oldest university in the United States. Where certification applies, each institution certifies its own part.'),
        ('Are the online courses the university’s own?',
         'Yes. Pre-designed and blended programs use courses from the university’s own online professional learning platform, and certificates are issued by the institution itself.'),
    ],
}

# ---------------------------------------------------------------- catalog
AREAS = [
    ("ai",       "Inteligencia artificial y datos",              "Artificial intelligence and data"),
    ("emerging", "Tecnologías emergentes",                       "Emerging technologies"),
    ("cyber",    "Ciberseguridad",                               "Cybersecurity"),
    ("digital",  "Transformación digital e innovación",          "Digital transformation and innovation"),
    ("systems",  "Ingeniería, operaciones y cadena de suministro", "Engineering, operations and supply chain"),
    ("sustain",  "Sostenibilidad y ESG",                         "Sustainability and ESG"),
    ("bio",      "Biotecnología y ciencias de la vida",          "Biotechnology and life sciences"),
    ("fashion",  "Moda y retail",                                "Fashion and retail"),
    ("leader",   "Liderazgo y desarrollo directivo",             "Leadership and executive development"),
    ("personal", "Desarrollo personal",                          "Personal effectiveness"),
]

# (area, ES title, ES summary, EN title, EN summary)
TOPICS = [
    ("ai", "Inteligencia artificial",
     "Aprendizaje automático, redes neuronales y procesamiento del lenguaje natural, y cómo diseñar, implantar y evaluar sistemas de IA con criterio ético.",
     "Artificial intelligence",
     "Machine learning, neural networks and natural language processing, and how to design, implement and evaluate AI systems responsibly."),
    ("ai", "IA agéntica: sistemas de IA éticos y autónomos",
     "Sistemas de IA que actúan de forma autónoma: marcos éticos, autonomía, confianza y transparencia para liderar su desarrollo.",
     "Agentic AI: designing ethical, empowered AI systems",
     "AI systems that act autonomously: ethical frameworks, autonomy, trust and transparency for leading their development."),
    ("ai", "Aprendizaje automático",
     "Aprendizaje supervisado y no supervisado, selección y evaluación de modelos, aplicados a datos reales.",
     "Machine learning",
     "Supervised and unsupervised learning, model selection and evaluation, applied to real-world data."),
    ("ai", "Diseño y desarrollo de productos y servicios de IA",
     "Diseñar, desarrollar y desplegar productos basados en IA con diseño centrado en el usuario.",
     "Designing and building AI products and services",
     "Design, develop and deploy AI-powered products with user-centred design."),
    ("ai", "Ciencia de datos",
     "Recogida, limpieza, análisis y visualización de datos, estadística y big data para convertir los datos en decisiones.",
     "Data science",
     "Data collection, cleaning, analysis and visualisation, statistics and big data to turn data into decisions."),
    ("ai", "Certificado profesional en ciencia de datos y analítica",
     "Métodos estadísticos, aprendizaje automático y big data mediante proyectos prácticos.",
     "Professional certificate in data science and analytics",
     "Statistical methods, machine learning and big data through hands-on projects."),
    ("ai", "Algoritmos",
     "Diseño y análisis de algoritmos de ordenación, búsqueda, grafos y optimización para una computación eficiente.",
     "Algorithms",
     "Design and analysis of sorting, search, graph and optimisation algorithms for efficient computation."),

    ("emerging", "Realidad aumentada y virtual",
     "Tecnología y diseño de interfaces para experiencias inmersivas e interactivas.",
     "Augmented and virtual reality",
     "Technology and interface design for immersive, interactive experiences."),
    ("emerging", "Computación cuántica",
     "Cúbits, entrelazamiento y algoritmos cuánticos, y su potencial en criptografía, simulación y análisis de datos.",
     "Quantum computing",
     "Qubits, entanglement and quantum algorithms, and their potential in cryptography, simulation and data analysis."),
    ("emerging", "Internet de las cosas (IoT)",
     "Diseño y despliegue de sistemas IoT: sensores, conectividad, analítica de datos y seguridad de los dispositivos.",
     "Internet of Things (IoT)",
     "Design and deployment of IoT systems: sensors, connectivity, data analytics and device security."),
    ("emerging", "Aplicación y diseño de IoT",
     "Arquitectura, protocolos y gestión de datos de dispositivos conectados en industria, energía y salud.",
     "IoT application and design",
     "Architecture, protocols and data management for connected devices in manufacturing, energy and healthcare."),
    ("emerging", "Gemelos digitales",
     "Réplicas digitales de activos, procesos o sistemas para simularlos y mejorarlos.",
     "Digital twins",
     "Digital replicas of assets, processes or systems used to simulate and improve them."),
    ("emerging", "Electrónica de estado sólido",
     "Dispositivos semiconductores, como diodos y transistores, y su fabricación y uso en la electrónica actual.",
     "Solid-state electronics",
     "Semiconductor devices such as diodes and transistors, and how they are made and used in modern electronics."),
    ("emerging", "Materiales avanzados",
     "Materiales compuestos, polímeros y nanomateriales y sus aplicaciones en electrónica, aeroespacial y medicina.",
     "Advanced materials",
     "Composites, polymers and nanomaterials and their applications in electronics, aerospace and medicine."),

    ("cyber", "Certificado profesional en ciberseguridad",
     "Seguridad de redes, criptografía, detección de amenazas y respuesta a incidentes, con estrategias de defensa.",
     "Professional certificate in cybersecurity",
     "Network security, cryptography, threat detection and incident response, with defence strategies."),

    ("digital", "Transformación digital",
     "Cómo la tecnología cambia los modelos de negocio: estrategia digital, experiencia de cliente, automatización y decisiones basadas en datos.",
     "Digital transformation",
     "How technology reshapes business models: digital strategy, customer experience, automation and data-driven decisions."),
    ("digital", "Innovación técnica: de la estrategia a la aplicación",
     "El ciclo completo de la innovación, desde detectar oportunidades hasta prototipar, validar en el mercado y escalar.",
     "Technical innovation: from strategy to application",
     "The full innovation lifecycle, from spotting opportunities to prototyping, market fit and scaling."),
    ("digital", "Innovación",
     "Marcos para generar y evaluar ideas, gestionar el proceso de innovación y crear una cultura de mejora continua.",
     "Innovation",
     "Frameworks to generate and evaluate ideas, manage the innovation process and build a culture of continuous improvement."),
    ("digital", "Pensamiento creativo",
     "Técnicas de generación de ideas, pensamiento lateral y resolución de problemas aplicadas al trabajo.",
     "Creative thinking",
     "Idea generation, lateral thinking and problem-solving techniques applied at work."),

    ("systems", "Arquitectura e ingeniería de sistemas: modelos y métodos para sistemas complejos (serie de 4 cursos)",
     "Arquitectura de sistemas, gestión del ciclo de vida y modelado para diseñar y gestionar sistemas complejos.",
     "Architecture and systems engineering: models and methods to manage complex systems (4-course series)",
     "System architecture, lifecycle management and modelling to design and manage complex systems."),
    ("systems", "Pensamiento sistémico",
     "Un enfoque global para resolver problemas: patrones, bucles de retroalimentación e interdependencias.",
     "Systems thinking",
     "A holistic approach to problem-solving: patterns, feedback loops and interdependencies."),
    ("systems", "Ingeniería de sistemas",
     "Análisis de requisitos, modelado, integración y verificación a lo largo del ciclo de vida.",
     "Systems engineering",
     "Requirements analysis, modelling, integration and verification across the life cycle."),
    ("systems", "Certificado profesional en gestión de proyectos técnicos",
     "Planificación, asignación de recursos y gestión de riesgos en proyectos técnicos, con metodologías ágiles y scrum.",
     "Professional certificate in technical project management",
     "Planning, resource allocation and risk management for technical projects, with agile and scrum methods."),
    ("systems", "Fabricación aditiva",
     "Impresión 3D y otros procesos aditivos: diseño, materiales y aplicaciones industriales.",
     "Additive manufacturing",
     "3D printing and other additive processes: design, materials and industrial applications."),
    ("systems", "Fabricación",
     "Procesos tradicionales, planificación de la producción, control de calidad, automatización y sistemas industriales.",
     "Manufacturing",
     "Traditional processes, production planning, quality control, automation and industrial systems."),
    ("systems", "Cadena de suministro digital",
     "Cómo blockchain, IoT e IA permiten visibilidad integral, analítica predictiva y gestión del riesgo en la cadena de suministro.",
     "Digital supply chain",
     "How blockchain, IoT and AI enable end-to-end visibility, predictive analytics and risk management across the supply chain."),
    ("systems", "Gestión de la cadena de suministro",
     "Planificación y gestión de la cadena de suministro.",
     "Supply chain management",
     "Planning and managing the supply chain."),
    ("systems", "Diseño de la cadena de suministro",
     "Cadenas de suministro eficientes y resilientes: inventario, logística y previsión de la demanda.",
     "Supply chain design",
     "Efficient, resilient supply chains: inventory, logistics and demand forecasting."),

    ("sustain", "ESG: ambiental, social y gobernanza",
     "Finanzas sostenibles, relación con grupos de interés, transparencia y estrategias para integrar criterios ESG.",
     "ESG: environmental, social and governance",
     "Sustainable finance, stakeholder engagement, transparency and strategies to integrate ESG standards."),
    ("sustain", "Objetivos de Desarrollo Sostenible (ODS)",
     "Los ODS de Naciones Unidas y cómo alinear con ellos las iniciativas de negocio y de política pública.",
     "Sustainable Development Goals (SDGs)",
     "The UN Sustainable Development Goals and how to align business and policy initiatives with them."),
    ("sustain", "Descarbonización",
     "Captura de carbono, energías renovables, transporte sostenible y eficiencia energética para reducir emisiones.",
     "Decarbonization",
     "Carbon capture, renewables, sustainable transport and energy efficiency to cut emissions."),
    ("sustain", "Sostenibilidad",
     "Gestión de recursos, análisis de ciclo de vida y economía circular para diseñar sistemas resilientes.",
     "Sustainability",
     "Resource management, life-cycle analysis and the circular economy to design resilient systems."),

    ("bio", "Edición genómica",
     "CRISPR y otras técnicas de edición genómica, sus usos en biotecnología y medicina, y sus retos éticos y regulatorios.",
     "Genome editing",
     "CRISPR and other genome-editing techniques, their uses in biotechnology and medicine, and their ethical and regulatory challenges."),
    ("bio", "Biotecnología",
     "Ingeniería genética, bioinformática y desarrollo de fármacos aplicados a la medicina, la agricultura y el medio ambiente.",
     "Biotechnology",
     "Genetic engineering, bioinformatics and drug development applied to medicine, agriculture and the environment."),

    ("fashion", "Distribución IoT en moda y retail",
     "El internet de las cosas aplicado a la distribución en el sector de la moda y el retail.",
     "Fashion and retail IoT distribution",
     "The Internet of Things applied to distribution in the fashion and retail sector."),
    ("fashion", "IA aplicada a moda y retail",
     "Aplicaciones de la inteligencia artificial en el sector de la moda y el retail.",
     "AI applied to fashion and retail",
     "Applications of artificial intelligence in the fashion and retail sector."),
    ("fashion", "Realidad aumentada y virtual para diseño y retail",
     "Realidad aumentada y virtual aplicadas al diseño y al retail.",
     "AR/VR for design and retail",
     "Augmented and virtual reality applied to design and retail."),

    ("leader", "Descubrir y aplicar sus fortalezas de liderazgo",
     "Inteligencia emocional, comunicación y motivación de equipos para desarrollar un estilo de liderazgo propio.",
     "Discovering and implementing your leadership strengths",
     "Emotional intelligence, communication and team motivation to develop your own leadership style."),
    ("leader", "Estrategia y capacidades de la organización",
     "Alinear recursos con objetivos estratégicos mediante marcos de análisis competitivo y ejecución.",
     "Understanding organizational strategy and capabilities",
     "Align resources with strategic goals using frameworks for competitive analysis and execution."),
    ("leader", "Cultura y redes en la organización",
     "Entender la cultura y las redes informales para crear alianzas e impulsar el cambio.",
     "Navigating and leveraging culture and networks",
     "Understand culture and informal networks to build alliances and drive change."),
    ("leader", "Influencia y poder",
     "Cómo influyen las dinámicas de poder en el trabajo y cómo gestionar grupos de interés y crear apoyos.",
     "Navigating and applying influence and power",
     "How power dynamics shape the workplace, and how to manage stakeholders and build support."),
    ("leader", "Liderar equipos",
     "Comunicación, resolución de conflictos y gestión del desempeño para liderar equipos diversos.",
     "Leading teams",
     "Communication, conflict resolution and performance management for leading diverse teams."),
    ("leader", "Equipos de alto rendimiento",
     "Dinámicas de equipo, motivación y métricas para crear y liderar equipos de alto rendimiento.",
     "High-performance teams",
     "Team dynamics, motivation and metrics to build and lead high-performing teams."),
    ("leader", "Influir sin autoridad",
     "Relación, comunicación y persuasión para liderar iniciativas sin autoridad formal.",
     "Influence without authority",
     "Rapport, communication and persuasion to lead initiatives without formal authority."),
    ("leader", "Delegar y empoderar",
     "Delegación eficaz, confianza y responsabilidad para que los equipos asuman sus resultados.",
     "Delegating and empowering",
     "Effective delegation, trust and accountability so teams own their results."),
    ("leader", "Liderazgo emprendedor",
     "Visión, gestión del riesgo, resiliencia y movilización de recursos para liderar nuevos proyectos.",
     "Entrepreneurial leadership",
     "Vision-setting, risk management, resilience and resource mobilisation for leading new ventures."),
    ("leader", "Toma de decisiones",
     "Marcos y herramientas para decidir con información, gestionar el riesgo y evitar errores frecuentes.",
     "Decision making",
     "Frameworks and tools for informed decisions, managing risk and avoiding common pitfalls."),
    ("leader", "Diversidad e inclusión",
     "Crear entornos inclusivos y aprovechar la diversidad de perspectivas para innovar.",
     "Diversity and inclusion",
     "Build inclusive environments and use diverse perspectives to innovate."),

    ("personal", "Mindfulness y bienestar",
     "Técnicas de atención plena, gestión del estrés y resiliencia para la vida personal y profesional.",
     "Mindfulness and wellness",
     "Mindfulness, stress management and resilience techniques for personal and professional life."),
    ("personal", "Autoconocimiento",
     "Identificar fortalezas, valores y estilos de decisión para mejorar la eficacia y las relaciones.",
     "Building self-awareness",
     "Identify strengths, values and decision-making styles to improve effectiveness and relationships."),
    ("personal", "Entender sus sesgos",
     "Reconocer los sesgos conscientes e inconscientes para tomar decisiones más justas.",
     "Understanding your biases",
     "Recognise conscious and unconscious biases to make fairer decisions."),
    ("personal", "Desarrollar la experiencia",
     "Práctica deliberada y aprendizaje estructurado para profundizar en su especialidad.",
     "Building expertise",
     "Deliberate practice and structured learning to deepen your expertise."),
    ("personal", "Mentalidad de crecimiento",
     "Afrontar retos, aprender del feedback y desarrollar resiliencia.",
     "Growth mindset",
     "Embrace challenges, learn from feedback and build resilience."),
]

FREQUENT_THEMES = {
    "es": ["IA generativa, IA agéntica y automatización: qué es cada una",
           "Priorización de casos de uso de IA según objetivos de negocio y riesgo",
           "Por qué fracasan los proyectos de IA en las grandes organizaciones",
           "Gobernanza de la IA y marco regulatorio europeo",
           "Liderazgo de equipos que trabajan con IA",
           "Diseño de agentes de IA con supervisión humana",
           "Procesos de innovación para pasar de la idea al despliegue"],
    "en": ["Generative AI, agentic AI and automation: what each one is",
           "Prioritizing AI use cases by business objectives and risk",
           "Why AI initiatives fail in large organizations",
           "AI governance and the European regulatory framework",
           "Leading teams that work with AI",
           "Designing AI agents with human oversight",
           "Innovation processes to move from idea to deployment"],
}

# ---------------------------------------------------------------- media
# Drop files into ./media with these names (jpg, png or webp; any size >= 1800px wide)
# and run build.py: the site creates optimized WebP versions automatically.
# Missing files show a brand block (fog + hexagon mark + yellow stem rule).
MEDIA = {
    "home-intro":        ("4 / 5",  "Directivos trabajando en grupo durante un taller de formación", "Executives working together during a training workshop"),
    "home-partnerships": ("16 / 9", "Profesorado universitario explicando en un aula",                "University faculty teaching in a classroom"),
    "home-camps":        ("16 / 9", "Estudiantes trabajando en un proyecto tecnológico",              "Students working on a technology project"),
    "courses-hero":      ("4 / 3",  "Profesor impartiendo una sesión a un grupo de directivos",       "Faculty member leading a session with executives"),
    "courses-delivery":  ("21 / 9", "Grupo de profesionales en una sesión de formación presencial",    "Group of professionals in an in-person training session"),
    "partners-hero":     ("4 / 3",  "Profesor dando clase en un aula universitaria",                   "Professor teaching in a university lecture hall"),
    "camps-hero":        ("4 / 3",  "Estudiantes preuniversitarios construyendo un proyecto",         "Pre-university students building a project"),
    "camps-campus":      ("21 / 9", "Estudiantes atendiendo a una clase en un aula universitaria",      "Students attending a class in a university lecture hall"),
    "about-hero":        ("4 / 3",  "Equipo colaborando en una reunión de trabajo",                   "Team collaborating in a working session"),
}
# Royalty-free sources, all checked on their source page (free commercial use, no attribution required).
# The site loads them from the source while media/ is empty; run fetch_media.py to self-host them.
_EXEC = ("https://images.unsplash.com/photo-1758518730083-4c12527b6742", "https://unsplash.com/photos/7Nu4atuZN1U")
_WORKSHOP = ("https://images.unsplash.com/photo-1758873268998-2f77c2d38862", "https://unsplash.com/photos/rgKX4o2xSqI")
_LECTURE = ("https://images.unsplash.com/photo-1758270704602-9d4103704ad4", "https://unsplash.com/photos/nrE0LK_qN7E")
_STUDENTS = ("https://images.unsplash.com/photo-1758270705290-62b6294dd044", "https://unsplash.com/photos/kp7qkHTgSKc")
MEDIA_SOURCES = {
    "home-intro": _EXEC, "home-partnerships": _LECTURE, "home-camps": _STUDENTS,
    "courses-hero": _WORKSHOP, "courses-delivery": _EXEC, "partners-hero": _LECTURE,
    "camps-hero": _STUDENTS, "camps-campus": _LECTURE, "about-hero": _WORKSHOP,
}
HERO_VIDEO_SOURCE = {
    "mp4": "https://assets.mixkit.co/videos/42643/42643-720.mp4",
    "poster": "https://assets.mixkit.co/videos/42643/42643-thumb-720-0.jpg",
    "page": "https://mixkit.co/free-stock-video/presentation-in-a-business-meeting-room-42643/",
}
# Hero video: media/hero.mp4 (required for video), media/hero.webm (optional),
# media/hero-mobile.mp4 (optional, vertical), media/hero-poster.jpg (recommended).
