# Medinder: SEO, ASO and AI-search plan

Goal: page one on Google, the App Store and AI answers for medication and pill reminder searches, in all 18 app languages, as fast as possible.

Being honest about speed: big terms like "pill reminder app" belong to Medisafe, MyTherapy, Apple and big review sites. A new domain usually needs **6–12 months** and real backlinks to reach page one for those, and nobody can guarantee it. Long, specific searches ("every 8 hours medication schedule", "medication reminder that rings on silent") can rank in **weeks to 3 months**. So the plan wins the long tail first, then uses that traffic and those links to move up on the big terms.

---

## 1. Launch checklist (week 1)

| # | Step | Who |
|---|---|---|
| 1 | Buy **medinder.app** (and medinder.com to redirect to it). Both were unregistered on 2026-11-09. If you choose another domain, change `SITE` in `build.py`. | You |
| 2 | Live on **GitHub Pages** at https://e1iaas.github.io/medinder-website/, rebuilt on every push to `main`. Once medinder.app is bought, add it as the custom domain in the repo's Pages settings and set `SITE` in `build.py` to `https://medinder.app`. | You |
| 3 | App Store Connect → App Information: **Privacy Policy URL** `https://medinder.app/privacy/`, **Support URL** `https://medinder.app/support/`, **Marketing URL** `https://medinder.app/`. Each language has its own pages (`/de/privacy/` and so on) if you want localized URLs per localization. | You |
| 4 | Verify the domain in **Google Search Console** and **Bing Webmaster Tools** and submit `https://medinder.app/sitemap.xml`. Bing matters for AI search: ChatGPT search and Copilot use its index. In Bing, also turn on IndexNow. | You |
| 5 | When the app is live, put its numeric ID in `APP_ID` in `build.py` and rebuild. That turns every "Coming soon" into a real App Store link and adds the Smart App Banner on iPhone. | Claude |
| 6 | Paste the App Store name, subtitle and keywords for each language from `ASO_KEYWORDS.md` into App Store Connect. | You |
| 7 | Add your legal name (or company) to the privacy policy. EU privacy law (GDPR) requires the controller to be named. | You |

## 2. What is already built

- **180 pages**: 10 pages × 18 languages, each with its own URL (`/`, `/de/`, `/ja/` …).
- Pages: home, privacy policy, support (both linked to eliastestdev@gmail.com), 2 free tools, 3 guides, and index pages for tools and guides.
- **Mobile first**: no framework, about 11 KB of HTML and one 6 KB stylesheet per page, a 48 KB hero image, system fonts, 48 px tap targets, large text, dark mode, right-to-left layout for Arabic.
- **Technical SEO**: a canonical URL and `hreflang` links to all 18 languages plus `x-default` on every page, `sitemap.xml` with every language version, `robots.txt`, Open Graph and share image, breadcrumbs.
- **Structured data**: `MobileApplication`, `Organization`, `FAQPage`, `Article`, `WebApplication` for the tools, `BreadcrumbList`.
- **AI search**: `llms.txt` with plain facts and every page, robots.txt that explicitly lets GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended and Applebot-Extended in, and short question-and-answer blocks that AI tools can quote directly.
- **Local wording**: every language was written with the words people there actually search for, not translated word for word. Its target keywords are in `ASO_KEYWORDS.md`.

## 3. Keyword strategy

Keywords per language are in `ASO_KEYWORDS.md`. English clusters, in the order to win them:

| Priority | Cluster | Example searches | Page type | Why it can win fast |
|---|---|---|---|---|
| 1 | Dose time maths | every 8 hours medication schedule, every 6 hours what times, twice a day medication times, every 12 hours schedule | Tool + one page per interval | Simple question, weak answers today, tools get links |
| 2 | Printables | printable medication schedule, pill chart template, medication log sheet, medication list for wallet | Tool | Evergreen, high volume, caregivers share them |
| 3 | Rings on silent | medication reminder that rings on silent, pill alarm iPhone, medication alarm app | Guide + home | Medinder's unique strength (AlarmKit); few pages target it |
| 4 | Older adults and caregivers | pill reminder app for elderly, medication reminder for seniors, simple medication app for older adults, medication reminders for elderly parents | Guide + home | Clear audience match; big sites write generic pages |
| 5 | iPhone how-to | how to set medication reminders on iPhone, Health app medication reminders not working, medication widget iPhone | Guide | People hit problems after iOS updates; fresh content wins |
| 6 | Privacy | medication tracker no account, private pill reminder app | Home + privacy | Few competitors can honestly claim it |
| 7 | Comparisons | Medisafe alternative, MyTherapy alternative, best pill reminder app for iPhone 2026 | Comparison pages | Buyers at decision time; write them after cluster 1–4 have links |
| 8 | Head terms | pill reminder app, medication reminder app, medication tracker app | Home | Needs authority from all of the above |

**Rules for every new page:** one main search phrase in the title, H1, first sentence and URL; answer the question in the first two sentences (good for Google snippets and AI answers); a short question-and-answer block; links to one tool, one guide and the home page; under 15 words per sentence where possible.

## 4. Content and tools to add (12 weeks, 2–3 pages a week)

Each new page goes out in all 18 languages, written with that language's own search terms.

| Week | Page | Main search phrase | Type |
|---|---|---|---|
| 1 | Every 8 hours medication schedule | every 8 hours schedule | Interval page (uses the calculator) |
| 1 | Every 6 hours / every 12 hours / every 4 hours | every 6 hours medication times | 3 interval pages |
| 2 | Twice a day, three times a day, four times a day: what times? | 3 times a day medication times | Guide |
| 2 | Printable medication list (wallet card) | medication list template | Tool |
| 3 | Blood pressure log (printable) | blood pressure log printable | Tool, matches the app's measurements |
| 3 | Weekly pillbox planner | pill organizer chart | Tool |
| 4 | Medication reminder that rings on silent | medication alarm on silent | Guide |
| 4 | Every other day / weekly medication reminder | every other day medication schedule | Guide + calendar tool |
| 5 | Travel and time zones: medication times calculator | medication time zone travel | Tool |
| 5 | Health app medication reminders not working | iphone medication reminders not working | Troubleshooting guide |
| 6 | Pill reminder app for elderly: what to look for | pill reminder app for elderly | Buyer's guide |
| 6 | How to help a parent with dementia remember medication | dementia medication reminder | Caregiver guide (no medical advice) |
| 7–8 | Medisafe alternative, MyTherapy alternative, best pill reminder apps for iPhone | best pill reminder app iphone | Honest comparisons, facts checked |
| 9–12 | Common questions per medication type: "how to remember eye drops", "how to remember vitamin D", "how to remember weekly tablets" | how to remember to take vitamins | Short guides |

Interval pages and "how to remember X" pages are programmatic SEO: one template, many real search questions. Keep each page genuinely useful with a working example, or Google treats them as thin.

## 5. Trust signals (essential for health topics)

Google holds health pages to a higher bar (it calls this YMYL, "your money or your life"). Without trust signals, health pages from a new site rank slowly.

1. Have a **pharmacist or nurse review the guides** and name them on each guide ("Reviewed by …, licensed pharmacist"). This is the single biggest boost for this topic.
2. Add an **About page** with you, why you built Medinder, and your country.
3. Keep "Last updated" dates current and refresh every guide every 6 months.
4. Link to official sources (NHS, FDA, national medicine agencies in each country) where a guide states a fact.
5. Never give dosing advice. The site already points every dosing question to the doctor, pharmacist or leaflet.

## 6. Links (how pages climb faster)

- **Tools as link magnets**: email caregiver blogs, senior centres, home-care companies, patient associations and pharmacy blogs in each country. Offer the printable schedule and blood pressure log as free resources for them to link to.
- **Directories**: AlternativeTo (as an alternative to Medisafe and MyTherapy), Product Hunt launch, Indie Hackers, local "made in Sweden" app lists.
- **Press**: a short story for Swedish tech and senior press ("Swedish developer builds a pill reminder that rings like an alarm"), then the same pitch to senior and health journalists in each language market.
- **Expert quotes**: answer journalist requests about medication reminders and seniors on Qwoted or Featured.
- **Communities**: answer real questions on Reddit (r/CaregiverSupport, r/AgingParents, r/iphone) and Quora, and only link where the tool truly answers the question. AI answers quote these communities heavily.
- Don't buy links. For health sites it can get the whole domain demoted.

## 7. AI search (ChatGPT, Perplexity, Google AI Overviews, Claude)

- AI tools cite pages that **answer in one clear sentence**, appear in the **Bing and Google indexes**, and are **mentioned by other sites**. The site covers the first two. Section 6 covers the third.
- Get Medinder into "best medication reminder apps 2026" articles. AI answers lean on those lists. Email the authors of the top 10 results in each language when the app is live.
- Keep `llms.txt` and the key facts in the home page FAQ in sync with the app (iOS version, languages, price model).
- Every month, ask ChatGPT, Perplexity and Google "best pill reminder app for elderly iPhone" in 3–4 languages and note whether Medinder appears and which sources are cited. Then go after those sources.

## 8. App Store (ASO)

- **Metadata per language** is in `ASO_KEYWORDS.md`: name and subtitle (30 characters each) and the keyword field (100 characters). In the keyword field, words are separated by commas with no spaces, with no repeats and no words already in the name or subtitle.
- **Extra keywords for free**: each App Store country also searches some other localizations (for example, the US store also reads Spanish (Mexico) metadata). Fill those extra localizations with different English keywords to double the coverage.
- **Screenshots**: localize the caption text into all 18 languages. The first two screenshots carry the message: "Rings even on silent" and "Did I take it? One look".
- **Ratings**: ask for a rating after the user has tapped Taken on 7 different days, never during onboarding. Ratings and rating count matter a lot for App Store ranking.
- **Custom product pages**: one page for "for elderly parents" and one for "rings on silent", used with Apple Search Ads on those exact keywords.
- **Apple Search Ads**: start with exact-match bids on the long-tail English terms, measure which convert, then move those words into the keyword field.
- **In-App Events**: run one every few weeks (for example "Start a medication routine this week"). They show in search results.

## 9. Measuring

| What | Where | How often |
|---|---|---|
| Impressions, clicks and position per page, language and country | Google Search Console, Bing Webmaster Tools | Weekly |
| Keyword rankings for 20 terms per main language | Search Console's queries report, or a rank tracker | Weekly |
| App Store search impressions and downloads | App Store Connect → Analytics, by source "App Store Search" | Weekly |
| App Store keyword rank | Appfigures, AppTweak or Astro | Weekly |
| Whether AI answers mention Medinder | Manual check, section 7 | Monthly |

Expand what works: if an interval page ranks, build the next interval. If a language gets traffic, write more pages in it first.

## 10. How to edit the site

- All text lives in `content/<language>.json`. English (`en.json`) is the source.
- Run `python3 build.py`. It checks that every language has the same pages, links and FAQ count, then writes `public/` and `ASO_KEYWORDS.md`.
- To add a page: add it to `PATHS` in `build.py` and to every language file.
- The translations were written by AI and have not been reviewed by native speakers. Get the home page and the privacy policy reviewed first in your 3–4 biggest markets.
