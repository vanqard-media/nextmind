# -*- coding: utf-8 -*-
"""Legal notice and privacy policy texts (ES/EN). Each section is (heading, [paragraphs])."""
import os
from content import CONFIG as C, MEDIA_SOURCES

_MEDIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
def _have(name):
    return any(os.path.exists(os.path.join(_MEDIA, name + ext)) for ext in (".jpg", ".jpeg", ".png", ".webp", ".mp4"))
# True when fetch_media.py downloaded everything, so nothing loads from third-party servers.
SELF_HOSTED = all(_have(n) for n in MEDIA_SOURCES) and (_have("hero") or _have("hero-source"))
HOST_ES = ("Las tipografías, imágenes y vídeos se sirven desde nuestro propio sitio web." if SELF_HOSTED else
           "Las tipografías se sirven desde nuestro propio sitio web. Algunas imágenes y el vídeo de portada se cargan desde los servidores de Unsplash y Mixkit, que pueden recibir la dirección IP del visitante para entregarlos.")
HOST_EN = ("Fonts, images and videos are served from our own website." if SELF_HOSTED else
           "Fonts are served from our own website. Some images and the cover video are loaded from Unsplash and Mixkit servers, which may receive the visitor's IP address in order to deliver them.")

ADDR_ES = f'{C["street"]}, {C["postal_code"]} {C["city"]} ({C["country"]})'
ADDR_EN = f'{C["street"]}, {C["postal_code"]} {C["city"]} (Spain)'
REG_ES = f' Inscrita en el {C["registry"]}.' if C.get("registry") else ""
REG_EN = f' Registered in the {C["registry"]}.' if C.get("registry") else ""
UPDATED = {"es": "Última actualización: 20 de octubre de 2026.", "en": "Last updated: 20 October 2026."}

LEGAL = {
 "es": dict(
  title="Aviso legal | NextMind Learning",
  desc="Aviso legal de nextmindlearning.com: datos del titular, condiciones de uso, propiedad intelectual y legislación aplicable.",
  h1="Aviso legal",
  lead="Información sobre el titular de este sitio web y las condiciones de uso, conforme a la Ley 34/2002 de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE).",
  sections=[
   ("Titular del sitio web", [
     f'Denominación social: {C["legal_name"]}',
     f'NIF: {C["tax_id"]}',
     f'Domicilio: {ADDR_ES}',
     f'Correo electrónico: {C["email"]}' + REG_ES]),
   ("Objeto", ["Este sitio web informa sobre los servicios de formación ejecutiva, consultoría, alianzas universitarias y campamentos de NextMind Learning. Su uso atribuye la condición de usuario e implica la aceptación de este aviso legal."]),
   ("Condiciones de uso", ["El usuario se compromete a hacer un uso adecuado del sitio web y de sus contenidos, de acuerdo con la ley, la buena fe y el orden público, y a no emplearlos para actividades ilícitas o que puedan dañar a NextMind Learning o a terceros.",
     "La información de este sitio web tiene carácter informativo y no constituye una oferta vinculante. Las condiciones de cada servicio se establecen en la propuesta correspondiente."]),
   ("Propiedad intelectual e industrial", ["Los textos, el diseño, la marca, el logotipo y el resto de contenidos propios de este sitio web pertenecen a NextMind Learning S.L. o se utilizan con autorización. No se permite su reproducción, distribución o transformación sin autorización previa por escrito.",
     "Las fotografías proceden de Unsplash y el vídeo de Mixkit, y se utilizan conforme a sus respectivas licencias. Las tipografías Archivo y Archivo Expanded se distribuyen bajo la licencia SIL Open Font License."]),
   ("Responsabilidad", ["NextMind Learning procura que la información publicada sea correcta y esté actualizada, pero no garantiza la ausencia de errores ni la disponibilidad continua del sitio web, y no se responsabiliza de los daños derivados de su uso, salvo en los casos previstos por la ley."]),
   ("Enlaces", ["Este sitio web puede contener enlaces a sitios de terceros. NextMind Learning no controla esos sitios ni se hace responsable de sus contenidos."]),
   ("Protección de datos y cookies", ["El tratamiento de los datos personales se explica en la política de privacidad. Este sitio web no utiliza cookies de análisis ni de publicidad."]),
   ("Legislación aplicable y jurisdicción", ["Este aviso legal se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales de Madrid, salvo que la normativa aplicable establezca otro fuero, como el del domicilio del consumidor."]),
  ]),
 "en": dict(
  title="Legal notice | NextMind Learning",
  desc="Legal notice for nextmindlearning.com: owner details, terms of use, intellectual property and governing law.",
  h1="Legal notice",
  lead="Information about the owner of this website and its terms of use, in accordance with Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE).",
  sections=[
   ("Website owner", [
     f'Company name: {C["legal_name"]}',
     f'Tax ID (NIF): {C["tax_id"]}',
     f'Registered address: {ADDR_EN}',
     f'Email: {C["email"]}' + REG_EN]),
   ("Purpose", ["This website provides information about NextMind Learning's executive education, consulting, university partnership and camp services. Using it makes you a user and implies acceptance of this legal notice."]),
   ("Terms of use", ["Users agree to use the website and its content appropriately, in accordance with the law, good faith and public order, and not to use them for unlawful activities or in ways that could harm NextMind Learning or third parties.",
     "The information on this website is for information purposes only and is not a binding offer. The terms of each service are set out in the corresponding proposal."]),
   ("Intellectual and industrial property", ["The texts, design, brand, logo and other original content of this website belong to NextMind Learning S.L. or are used with permission. They may not be reproduced, distributed or transformed without prior written authorization.",
     "Photographs come from Unsplash and the video from Mixkit, and are used under their respective licenses. The Archivo and Archivo Expanded typefaces are distributed under the SIL Open Font License."]),
   ("Liability", ["NextMind Learning strives to keep the information on this website accurate and up to date, but does not guarantee that it is error-free or continuously available, and is not liable for damages arising from its use, except where the law provides otherwise."]),
   ("Links", ["This website may contain links to third-party sites. NextMind Learning does not control those sites and is not responsible for their content."]),
   ("Data protection and cookies", ["The processing of personal data is explained in the privacy policy. This website does not use analytics or advertising cookies."]),
   ("Governing law and jurisdiction", ["This legal notice is governed by Spanish law. Any dispute shall be submitted to the courts of Madrid, unless applicable law establishes another venue, such as the consumer's place of residence.",
     "This English version is provided for convenience; in case of discrepancy, the Spanish version prevails."]),
  ]),
}

PRIVACY = {
 "es": dict(
  title="Política de privacidad | NextMind Learning",
  desc="Cómo trata NextMind Learning los datos personales de quienes contactan a través de nextmindlearning.com, conforme al RGPD y la LOPDGDD.",
  h1="Política de privacidad",
  lead="Cómo tratamos los datos personales que nos facilita a través de este sitio web, conforme al Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).",
  sections=[
   ("Responsable del tratamiento", [
     f'{C["legal_name"]}, NIF {C["tax_id"]}',
     f'Domicilio: {ADDR_ES}',
     f'Correo electrónico: {C["email"]}']),
   ("Qué datos tratamos", ["Los que usted nos facilita al escribirnos por correo electrónico o mediante el formulario de contacto: nombre y apellidos, empresa o institución, cargo, correo electrónico, teléfono (opcional), servicio de interés y el contenido de su mensaje.",
     "No recogemos categorías especiales de datos. Le rogamos que no las incluya en su mensaje."]),
   ("Para qué los usamos", ["Para responder a su consulta, enviarle la información o la propuesta que solicite y, en su caso, gestionar la relación precontractual y contractual con su organización."]),
   ("Base jurídica", ["Su consentimiento, que otorga al enviar el formulario o escribirnos (artículo 6.1.a del RGPD), y la aplicación de medidas precontractuales a petición suya (artículo 6.1.b del RGPD). Puede retirar su consentimiento en cualquier momento, sin que ello afecte a la licitud del tratamiento anterior."]),
   ("Cuánto tiempo los conservamos", ["Mientras sea necesario para atender su consulta y, si se establece una relación con su organización, mientras esta se mantenga. Después, los conservaremos bloqueados durante los plazos de prescripción de las responsabilidades legales que pudieran derivarse, y finalmente los suprimiremos."]),
   ("Quién puede acceder a ellos", ["No cedemos sus datos a terceros, salvo obligación legal.",
     "Para prestar el servicio utilizamos proveedores que actúan como encargados del tratamiento: Formspree (gestión del formulario de contacto), GitHub (alojamiento del sitio web) y Google (correo electrónico corporativo). Algunos de estos proveedores pueden tratar datos fuera del Espacio Económico Europeo, en particular en Estados Unidos. En esos casos, las transferencias se realizan con las garantías previstas en el RGPD, como el Marco de Privacidad de Datos UE-EE. UU. o las cláusulas contractuales tipo aprobadas por la Comisión Europea, según corresponda a cada proveedor."]),
   ("Sus derechos", [f'Puede ejercer sus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad escribiendo a {C["email"]} o a nuestro domicilio, indicando el derecho que desea ejercer.',
     "Si considera que no hemos tratado sus datos correctamente, puede presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es)."]),
   ("Menores de edad", ["Si es menor de 14 años, necesitamos el consentimiento de su madre, padre o tutor legal para tratar sus datos. En ese caso, pídale que nos escriba en su nombre."]),
   ("Decisiones automatizadas", ["No tomamos decisiones automatizadas ni elaboramos perfiles con sus datos."]),
   ("Cookies", ["Este sitio web no utiliza cookies de análisis ni de publicidad, ni herramientas de seguimiento. " + HOST_ES,
     "Al enviar el formulario de contacto, es posible que se muestre una página de confirmación de Formspree, que se rige por su propia política de privacidad y de cookies."]),
   ("Seguridad", ["Aplicamos medidas técnicas y organizativas adecuadas para proteger sus datos. El sitio web funciona exclusivamente con conexión cifrada (HTTPS)."]),
   ("Cambios en esta política", ["Podemos actualizar esta política para adaptarla a cambios legales o en nuestros servicios. La versión vigente es siempre la publicada en esta página."]),
  ]),
 "en": dict(
  title="Privacy policy | NextMind Learning",
  desc="How NextMind Learning processes the personal data of people who contact us through nextmindlearning.com, under the GDPR and Spanish law.",
  h1="Privacy policy",
  lead="How we process the personal data you provide through this website, in accordance with Regulation (EU) 2016/679 (GDPR) and Spanish Organic Law 3/2018 (LOPDGDD).",
  sections=[
   ("Data controller", [
     f'{C["legal_name"]}, Tax ID (NIF) {C["tax_id"]}',
     f'Address: {ADDR_EN}',
     f'Email: {C["email"]}']),
   ("What data we process", ["The data you give us when you email us or use the contact form: full name, company or institution, job title, email address, phone number (optional), service of interest and the content of your message.",
     "We do not collect special categories of data. Please do not include them in your message."]),
   ("Why we use it", ["To answer your enquiry, send you the information or proposal you request and, where applicable, manage the pre-contractual and contractual relationship with your organization."]),
   ("Legal basis", ["Your consent, given when you submit the form or write to us (Article 6(1)(a) GDPR), and taking pre-contractual steps at your request (Article 6(1)(b) GDPR). You may withdraw your consent at any time, without affecting the lawfulness of prior processing."]),
   ("How long we keep it", ["For as long as needed to handle your enquiry and, if a relationship is established with your organization, for as long as it lasts. Afterwards, we keep it blocked for the limitation periods of any legal liabilities that may arise, and then delete it."]),
   ("Who can access it", ["We do not share your data with third parties unless legally required.",
     "To provide our services we use providers acting as data processors: Formspree (contact form handling), GitHub (website hosting) and Google (corporate email). Some of these providers may process data outside the European Economic Area, particularly in the United States. In such cases, transfers take place with the safeguards provided for in the GDPR, such as the EU-US Data Privacy Framework or the European Commission's standard contractual clauses, as applicable to each provider."]),
   ("Your rights", [f'You can exercise your rights of access, rectification, erasure, objection, restriction of processing and portability by writing to {C["email"]} or to our registered address, stating the right you wish to exercise.',
     "If you believe we have not processed your data properly, you can lodge a complaint with the Spanish Data Protection Agency (www.aepd.es)."]),
   ("Minors", ["If you are under 14, we need the consent of your parent or legal guardian to process your data. In that case, please ask them to write to us on your behalf."]),
   ("Automated decisions", ["We do not make automated decisions or create profiles with your data."]),
   ("Cookies", ["This website does not use analytics or advertising cookies, or tracking tools. " + HOST_EN,
     "When you submit the contact form, a Formspree confirmation page may be shown, which is governed by Formspree's own privacy and cookie policy."]),
   ("Security", ["We apply appropriate technical and organizational measures to protect your data. The website works exclusively over an encrypted connection (HTTPS)."]),
   ("Changes to this policy", ["We may update this policy to reflect legal changes or changes to our services. The current version is always the one published on this page.",
     "This English version is provided for convenience; in case of discrepancy, the Spanish version prevails."]),
  ]),
}
