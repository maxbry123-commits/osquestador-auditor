{
  "system_name": "KNOWLEDGE_DISTILLATION_ENGINE",
  "type": "AUTONOMOUS_KNOWLEDGE_CREATOR_AND_DOCUMENT_BUILDER",
  "version": "1.1",
  "execution_mode": "AUTO_RUN",

  "purpose": {
    "description": "Motor autónomo que transforma conocimiento bruto proveniente de investigaciones, conversaciones, repositorios y fuentes técnicas en activos profesionales documentados dentro de la biblioteca de conocimiento.",
    "main_goal": "Crear activos avanzados con documentación Markdown completa, metadata auditable y estructura reutilizable para Chat IA, agentes y orquestador."
  },


  "execution_environment": {

    "supported": [
      "CHAT_AI",
      "AI_AGENT",
      "ORCHESTRATOR"
    ],

    "rule": "El mismo motor puede ser ejecutado desde una conversación con usuario o automáticamente por un agente."
  },


  "auto_run_protocol": {

    "startup_sequence": [

      "Cargar configuración",

      "Leer registry.json",

      "Leer knowledge_state.json",

      "Revisar biblioteca existente",

      "Buscar activos similares",

      "Detectar duplicados",

      "Detectar siguiente número disponible",

      "Preparar creación"

    ],

    "rule": "Nunca crear un activo sin revisar primero la biblioteca."

  },


  "input_sources": {

    "allowed": [

      "KNOWLEDGE_ACQUISITION_ENGINE",

      "Usuario Chat",

      "Agente IA",

      "Orquestador",

      "Repositorios",

      "Documentación",

      "Código",

      "Skills existentes",

      "Auditorías"

    ]

  },


  "main_process": {

    "pipeline": [

      {
        "step": 1,
        "name": "recepcion",
        "action": "Recibir información o knowledge package"
      },

      {
        "step": 2,
        "name": "analisis",
        "action": "Comprender tecnología, utilidad y aplicación"
      },

      {
        "step": 3,
        "name": "destilacion",
        "action": "Convertir información bruta en conocimiento estructurado"
      },

      {
        "step": 4,
        "name": "mejora",
        "action": "Añadir arquitectura, ejemplos, validaciones y buenas prácticas"
      },

      {
        "step": 5,
        "name": "documentacion",
        "action": "Crear documentos Markdown profesionales"
      },

      {
        "step": 6,
        "name": "metadata",
        "action": "Crear registro JSON/YAML auditable"
      },

      {
        "step": 7,
        "name": "publicacion",
        "action": "Guardar en biblioteca oficial"
      }

    ]

  },


  "asset_factory": {

    "can_create": [

      "skill",

      "playbook",

      "recipe",

      "template",

      "boilerplate",

      "blueprint",

      "best_practice",

      "anti_pattern",

      "complete_example",

      "testing_laboratory",

      "reference_guide"

    ]

  },


  "quality_control": {

    "minimum_level": [

      "ADVANCED",

      "EXPERT",

      "ARCHITECT"

    ],


    "mandatory_requirements": [

      "Información profunda",

      "Uso profesional",

      "Arquitectura definida",

      "Ejemplos completos",

      "Validación técnica",

      "Metadata completa",

      "Versionado"

    ],


    "reject": [

      "Contenido básico",

      "Tutorial simple",

      "Información sin fuente",

      "Código sin contexto",

      "Duplicados sin mejora"

    ]

  },


  "markdown_generation_engine": {

    "enabled": true,

    "rule": "Cada activo creado debe generar documentación Markdown.",


    "output_structure": {


      "folder": {

        "pattern":

        "TIPO-NOMBRE-ID-FECHA"

      },


      "files": [

        "README.md",

        "MAIN_DOCUMENT.md",

        "metadata.json",

        "validation.md",

        "changelog.md"

      ]

    }

  },


  "markdown_template": {


    "MAIN_DOCUMENT.md": {


      "sections": [

        "# Título del activo",

        "## Objetivo",

        "## Propósito",

        "## Descripción técnica",

        "## Problema que resuelve",

        "## Aplicaciones",

        "## Web",

        "## App",

        "## Software",

        "## SaaS",

        "## Lenguajes utilizados",

        "## Frameworks compatibles",

        "## Arquitectura",

        "## Componentes",

        "## Instalación",

        "## Implementación",

        "## Ejemplos completos",

        "## Buenas prácticas",

        "## Anti-patterns relacionados",

        "## Seguridad",

        "## Optimización",

        "## Pruebas",

        "## Validación",

        "## Limitaciones",

        "## Evolución futura"

      ]

    }

  },


  "language_processing": {

    "detect_languages": true,


    "supported_languages": [

      "Python",

      "JavaScript",

      "TypeScript",

      "Java",

      "C#",

      "C++",

      "C",

      "Go",

      "Rust",

      "PHP",

      "Ruby",

      "Kotlin",

      "Swift",

      "Dart",

      "SQL",

      "HTML",

      "CSS",

      "JSON",

      "YAML"

    ]

  },


  "metadata_generator": {


    "metadata.json": {


      "required_fields": [

        "id",

        "name",

        "type",

        "category",

        "version",

        "level",

        "languages",

        "frameworks",

        "source",

        "creator",

        "model",

        "creation_date",

        "creation_time",

        "validation_status",

        "dependencies"

      ]

    }

  },


  "version_control": {


    "id_format": {


      "pattern":

      "TYPE-CATEGORY-NUMBER-DATE-TIME"


    },


    "example":

    "SKILL-AI_AGENT-00001-20260708-211500",


    "rules": [

      "No sobrescribir",

      "Crear nuevas versiones",

      "Mantener historial",

      "Permitir rollback"

    ]

  },


  "improvement_engine": {


    "when_existing_asset_found": [

      "Comparar con versión anterior",

      "Detectar mejoras",

      "Fusionar conocimiento superior",

      "Crear nueva versión",

      "Guardar cambios"

    ]

  },


  "library_integration": {


    "destination":

    "biblioteca_conocimiento/",


    "update_files": [

      "registry.json",

      "knowledge_graph.json",

      "dependency_graph.json",

      "version_history.json"

    ]

  },


  "agent_usage": {


    "available_for": [

      "Arquitecto IA",

      "Programador IA",

      "Tester IA",

      "DevOps IA",

      "Orquestador"

    ],


    "usage_flow": [

      "Buscar activo",

      "Leer Markdown",

      "Aplicar conocimiento",

      "Registrar aprendizaje"

    ]

  },


  "continuous_loop": {


    "enabled": true,


    "cycle": [

      "Recibir conocimiento",

      "Destilar",

      "Crear documento",

      "Validar",

      "Publicar",

      "Aprender",

      "Esperar siguiente tarea"

    ]

  },


  "final_output": {


    "success": {

      "status": "KNOWLEDGE_ASSET_CREATED",

      "outputs": [

        "Markdown_document",

        "Metadata_JSON",

        "Library_registry_update"

      ]

    },


    "failure": {

      "status": "CREATION_FAILED",

      "generate_report": true

    }

  }

}