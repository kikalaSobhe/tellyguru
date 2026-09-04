# telly.guru

A tiny personal site built with Hugo and deployed with GitHub Pages.

## Run it locally

Install Hugo on macOS:

```sh
brew install hugo
```

Start the local server:

```sh
hugo server
```

Open `http://localhost:1313`.

Create a production build with:

```sh
hugo --minify
```

The generated site is written to `public/`.

## Publish with GitHub Pages

1. Create a GitHub repository and push this project to its `main` branch.
2. In the repository, open **Settings > Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Let the included `hugo.yaml` workflow finish.
5. In **Settings > Pages**, enter `telly.guru` under **Custom domain** and save it before changing DNS.

Every later push to `main` rebuilds and publishes the site automatically.

## Connect the GoDaddy domain

In GoDaddy, open the DNS records for `telly.guru`. The domain currently has GoDaddy parking A records at `15.197.148.33` and `3.33.130.190`. Remove those two `@` records, then add these four A records:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | `185.199.108.153` |
| A | @ | `185.199.109.153` |
| A | @ | `185.199.110.153` |
| A | @ | `185.199.111.153` |

The current `www` record points back to `telly.guru`. Replace it with:

| Type | Name | Value |
| --- | --- | --- |
| CNAME | www | `YOUR_GITHUB_USERNAME.github.io` |

Replace `YOUR_GITHUB_USERNAME` with the owner of the GitHub repository. Do not include the repository name in this CNAME value.

DNS can take up to 24 hours to settle. Once GitHub shows the domain check as successful, enable **Enforce HTTPS** in **Settings > Pages**.

## Project structure

- `content/_index.md`: homepage metadata
- `layouts/index.html`: homepage markup
- `assets/css/main.css`: responsive design and dark mode
- `assets/js/main.js`: the local "guru" answer interaction
- `assets/images/`: original project artwork
- `.github/workflows/hugo.yaml`: automatic GitHub Pages deployment
