(() => {
  "use strict";

  const config = window.FFIDEO_CONFIG || {};
  const placeholder = /^__.+__$/;
  const liveRegion = document.querySelector("[data-live-region]");

  const announce = (message) => {
    if (!liveRegion) return;
    liveRegion.textContent = "";
    window.setTimeout(() => {
      liveRegion.textContent = message;
    }, 20);
  };

  document.querySelectorAll("[data-config-link]").forEach((link) => {
    const key = link.dataset.configLink;
    const value = config[key];
    const unavailable = !value || placeholder.test(value);

    if (unavailable) {
      link.setAttribute("aria-disabled", "true");
      link.classList.add("is-pending");
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const message = link.dataset.pendingMessage || "This link is not live yet.";
        announce(message);
        const original = link.querySelector("[data-action-label]");
        if (original) {
          const previous = original.textContent;
          original.textContent = link.dataset.pendingLabel || "Coming soon";
          window.setTimeout(() => {
            original.textContent = previous;
          }, 1800);
        }
      });
      return;
    }

    link.href = value;
    if (key === "releaseZipUrl") link.setAttribute("download", "");
    link.removeAttribute("aria-disabled");
  });

  const translations = {
    en: {
      "nav.tools": "10 tools",
      "nav.local": "Local by design",
      "nav.install": "Install",
      "nav.terms": "Terms",
      "hero.eyebrow": "Native macOS menu-bar utility",
      "hero.titleA": "Edit the video.",
      "hero.titleB": "Skip the editor.",
      "hero.lede": "Ten focused video operations, one compact menu-bar app. Drop in a file, choose the result, and keep every frame on your Mac.",
      "hero.download": "Download free trial",
      "hero.buy": "How the trial works",
      "hero.pendingDownload": "Release download coming soon",
      "hero.pendingCheckout": "Checkout coming soon",
      "hero.requirements": "macOS 13+ · Apple Silicon · local processing",
      "mock.local": "LOCAL SESSION",
      "mock.title": "What should happen?",
      "mock.input": "interview.mov",
      "mock.output": "interview — compact.mp4",
      "mock.status": "Ready to save",
      "proof.files": "Your files",
      "proof.filesDetail": "never leave the Mac",
      "proof.tools": "10 tools",
      "proof.toolsDetail": "without a timeline",
      "proof.price": "US$4.99",
      "proof.priceDetail": "one-time, when checkout opens",
      "preview.eyebrow": "The real app",
      "preview.title": "Ten direct actions. No timeline.",
      "preview.body": "This is the actual FFideo 1.0.0 menu running on macOS. The compact 380×540 interface stays one click away in the menu bar.",
      "preview.caption": "Actual release interface · English · dark mode",
      "tools.eyebrow": "A smaller surface area",
      "tools.title": "The ten things you reach for.",
      "tools.intro": "No project setup. No cloud queue. No sprawling timeline. FFideo turns common finishing jobs into direct, named actions.",
      "tool.1": "Reduce File Size",
      "tool.1d": "Choose a maximum size.",
      "tool.2": "Convert to MP4",
      "tool.2d": "Create a widely usable H.264 file.",
      "tool.3": "Compress to 1080p",
      "tool.3d": "Downscale without upscaling smaller sources.",
      "tool.4": "Compress to 720p",
      "tool.4d": "Make a compact sharing copy.",
      "tool.5": "Trim Video",
      "tool.5d": "Keep only the selected range.",
      "tool.6": "Join Videos",
      "tool.6d": "Combine clips in your chosen order.",
      "tool.7": "Extract Audio as MP3",
      "tool.7d": "Save the primary audio track.",
      "tool.8": "Extract Audio as M4A",
      "tool.8d": "Save AAC audio in an M4A file.",
      "tool.9": "Remove Audio",
      "tool.9d": "Export a silent MP4.",
      "tool.10": "Remove Metadata",
      "tool.10d": "Remove metadata and additional tracks.",
      "local.eyebrow": "Local means local",
      "local.title": "A short path from file to result.",
      "local.body": "FFideo reads the media you select and writes the result to the local destination you choose. This public build includes no cloud processing, analytics, or advertising.",
      "local.step1": "Choose",
      "local.step1d": "Select a file on your Mac.",
      "local.step2": "Process",
      "local.step2d": "FFmpeg runs inside the app bundle.",
      "local.step3": "Verify",
      "local.step3d": "The output is checked before commit.",
      "local.step4": "Save",
      "local.step4d": "The result lands where you chose.",
      "install.eyebrow": "Bootstrap release disclosure",
      "install.title": "Not notarized. Install deliberately.",
      "install.body": "The current artifact is ad-hoc signed and not notarized. macOS may require an explicit exception for the first launch. Do not disable Gatekeeper globally.",
      "install.one": "Verify SHA256SUMS supplied with the release.",
      "install.two": "Extract FFideo-1.0.0.zip.",
      "install.three": "Move FFideo.app to Applications.",
      "install.four": "Launch it. If macOS blocks it, open System Settings → Privacy & Security → Open Anyway.",
      "install.link": "Read full install notes",
      "price.eyebrow": "Simple on purpose",
      "price.title": "One small tool. One small price.",
      "price.body": "If checkout becomes available, FFideo Pro is planned at US$4.99 as a one-time purchase for FFideo 1.x. No subscription is promised or required.",
      "price.cta": "Checkout — US$4.99",
      "price.note": "Checkout is not live yet; the download includes five free exports.",
      "footer.tagline": "Express video work, in the menu bar.",
      "footer.privacy": "Privacy",
      "footer.eula": "EULA",
      "footer.refunds": "Refunds",
      "footer.install": "Install",
      "footer.source": "Release notes"
    },
    es: {
      "nav.tools": "10 herramientas",
      "nav.local": "Local por diseño",
      "nav.install": "Instalación",
      "nav.terms": "Términos",
      "hero.eyebrow": "Utilidad nativa para la barra de menús",
      "hero.titleA": "Edita el video.",
      "hero.titleB": "Evita el editor.",
      "hero.lede": "Diez operaciones de video enfocadas, en una app compacta para la barra de menús. Arrastra un archivo, elige el resultado y conserva cada fotograma en tu Mac.",
      "hero.download": "Descargar prueba gratis",
      "hero.buy": "Cómo funciona la prueba",
      "hero.pendingDownload": "La descarga estará disponible pronto",
      "hero.pendingCheckout": "El checkout estará disponible pronto",
      "hero.requirements": "macOS 13+ · Apple Silicon · procesamiento local",
      "mock.local": "SESIÓN LOCAL",
      "mock.title": "¿Qué quieres hacer?",
      "mock.input": "entrevista.mov",
      "mock.output": "entrevista — compacto.mp4",
      "mock.status": "Listo para guardar",
      "proof.files": "Tus archivos",
      "proof.filesDetail": "no salen de la Mac",
      "proof.tools": "10 herramientas",
      "proof.toolsDetail": "sin una línea de tiempo",
      "proof.price": "US$4.99",
      "proof.priceDetail": "pago único, cuando abra el checkout",
      "preview.eyebrow": "La app real",
      "preview.title": "Diez acciones directas. Sin línea de tiempo.",
      "preview.body": "Este es el menú real de FFideo 1.0.0 ejecutándose en macOS. La interfaz compacta de 380×540 queda a un clic en la barra de menús.",
      "preview.caption": "Interfaz real de la versión · inglés · modo oscuro",
      "tools.eyebrow": "Una superficie menor",
      "tools.title": "Las diez acciones que buscas.",
      "tools.intro": "Sin configurar proyectos. Sin cola en la nube. Sin una línea de tiempo interminable. FFideo convierte tareas habituales en acciones directas y claras.",
      "tool.1": "Reducir tamaño",
      "tool.1d": "Elige un tamaño máximo.",
      "tool.2": "Convertir a MP4",
      "tool.2d": "Crea un archivo H.264 compatible.",
      "tool.3": "Comprimir a 1080p",
      "tool.3d": "Reduce sin ampliar fuentes pequeñas.",
      "tool.4": "Comprimir a 720p",
      "tool.4d": "Crea una copia compacta para compartir.",
      "tool.5": "Recortar video",
      "tool.5d": "Conserva solo el tramo elegido.",
      "tool.6": "Unir videos",
      "tool.6d": "Combina clips en el orden elegido.",
      "tool.7": "Extraer audio en MP3",
      "tool.7d": "Guarda la pista de audio principal.",
      "tool.8": "Extraer audio en M4A",
      "tool.8d": "Guarda audio AAC en un archivo M4A.",
      "tool.9": "Eliminar audio",
      "tool.9d": "Exporta un MP4 sin audio.",
      "tool.10": "Eliminar metadatos",
      "tool.10d": "Elimina metadatos y pistas adicionales.",
      "local.eyebrow": "Local significa local",
      "local.title": "Un camino corto del archivo al resultado.",
      "local.body": "FFideo lee los archivos que seleccionas y guarda el resultado en el destino local que eliges. Esta versión pública no incluye procesamiento en la nube, analítica ni publicidad.",
      "local.step1": "Elegir",
      "local.step1d": "Selecciona un archivo de tu Mac.",
      "local.step2": "Procesar",
      "local.step2d": "FFmpeg se ejecuta dentro del paquete de la app.",
      "local.step3": "Verificar",
      "local.step3d": "El resultado se comprueba antes de guardarlo.",
      "local.step4": "Guardar",
      "local.step4d": "El resultado llega al destino elegido.",
      "install.eyebrow": "Aviso de la versión bootstrap",
      "install.title": "Sin notarizar. Instala conscientemente.",
      "install.body": "El artefacto actual tiene firma ad-hoc y no está notarizado. macOS puede exigir una excepción explícita en el primer inicio. No desactives Gatekeeper globalmente.",
      "install.one": "Verifica SHA256SUMS incluido con la versión.",
      "install.two": "Extrae FFideo-1.0.0.zip.",
      "install.three": "Mueve FFideo.app a Aplicaciones.",
      "install.four": "Ábrela. Si macOS la bloquea, abre Configuración del Sistema → Privacidad y seguridad → Abrir igualmente.",
      "install.link": "Leer instrucciones completas",
      "price.eyebrow": "Simple a propósito",
      "price.title": "Una herramienta pequeña. Un precio pequeño.",
      "price.body": "Si el checkout llega a estar disponible, FFideo Pro está previsto a US$4.99 como compra única para FFideo 1.x. No se promete ni se exige una suscripción.",
      "price.cta": "Checkout — US$4.99",
      "price.note": "El checkout aún no está activo; la descarga incluye cinco exportaciones gratis.",
      "footer.tagline": "Trabajo de video exprés, desde la barra de menús.",
      "footer.privacy": "Privacidad",
      "footer.eula": "EULA",
      "footer.refunds": "Reembolsos",
      "footer.install": "Instalación",
      "footer.source": "Notas de versión"
    }
  };

  const languageButtons = document.querySelectorAll("[data-language]");
  const translatable = document.querySelectorAll("[data-i18n]");

  const applyLanguage = (language) => {
    const dictionary = translations[language];
    if (!dictionary) return;
    document.documentElement.lang = language;
    translatable.forEach((element) => {
      const key = element.dataset.i18n;
      if (dictionary[key]) element.textContent = dictionary[key];
    });
    languageButtons.forEach((button) => {
      const active = button.dataset.language === language;
      button.setAttribute("aria-pressed", String(active));
    });
    try {
      window.localStorage.setItem("ffideo-language", language);
    } catch (_) {
      // The site remains usable when storage is unavailable.
    }
  };

  languageButtons.forEach((button) => {
    button.addEventListener("click", () => applyLanguage(button.dataset.language));
  });

  let savedLanguage = "en";
  try {
    savedLanguage = window.localStorage.getItem("ffideo-language") || "en";
  } catch (_) {
    savedLanguage = "en";
  }
  applyLanguage(savedLanguage === "es" ? "es" : "en");
})();
