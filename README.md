# FFideo launch site

Zero-build static launch site for **FFideo**, a native Apple Silicon macOS menu-bar video utility. The site uses plain HTML, CSS, and JavaScript; it has no package manager, external font, analytics script, secret, or runtime service dependency.

## Local preview

From this repository:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173/`.

Run the zero-dependency regression and structural checks:

```sh
python3 -m unittest scripts/test_check_site.py -v
python3 scripts/check_site.py
python3 scripts/check_site.py --check-external
```

The external mode requests every configured public HTTPS URL; use the structural command when working offline.

## Public links and checkout preparation

All outbound product links are centralized in [`assets/config.js`](assets/config.js). The public GitHub release and ZIP URLs are pinned to `v1.0.0`. The single checkout value remains a public placeholder, so the purchase button is statically and dynamically disabled until a verified Lemon Squeezy checkout or store URL is supplied.

Only set `checkoutUrl` to the final public HTTPS URL. Do not put API keys, signing secrets, webhook secrets, or other private values in browser configuration.

[`success.html`](success.html) is the manual post-purchase destination. It tells the buyer to retrieve and copy the issued license key from the Lemon Squeezy receipt email or My Orders, open FFideo, choose **Activate Pro**, and paste/activate the key. It does not parse checkout parameters, import keys, create accounts, receive webhooks, or claim automatic activation. Before enabling checkout, configure the Lemon Squeezy product to issue license keys, verify the receipt/My Orders flow, and configure the successful-purchase redirect only after the public site URL is final.

## GitHub Pages publishing instructions

The repository is prepared for the custom domain `ffideo.gesuvik.lol` through the committed [`CNAME`](CNAME) file. No remote or DNS change is performed by this repository.

1. Create a new empty GitHub repository for this site. Do not initialize it with a README, license, or `.gitignore`.
2. In this local repository, add the new GitHub repository as `origin`:

   ```sh
   git remote add origin git@github.com:YOUR_GITHUB_USER/ffideo-site.git
   ```

3. Push the deploy branch and deploy-candidate tag:

   ```sh
   git push -u origin main
   git push origin ffideo-site-v1.0.0-rc1
   ```

4. On GitHub, open **Settings → Pages**.
5. Under **Build and deployment**, choose **Deploy from a branch**.
6. Choose branch **main**, folder **/(root)**, then click **Save**.
7. Under **Custom domain**, enter exactly:

   ```text
   ffideo.gesuvik.lol
   ```

8. Configure DNS with the provider that hosts `gesuvik.lol`: create a `CNAME` record whose host/name is `ffideo` and whose target is `YOUR_GITHUB_USER.github.io`. Remove conflicting records for the same host before validating.
9. Wait for GitHub Pages to report that the DNS check succeeded. Then enable **Enforce HTTPS**.
10. Verify these public paths after deployment:

    ```text
    https://ffideo.gesuvik.lol/
    https://ffideo.gesuvik.lol/install.html
    https://ffideo.gesuvik.lol/privacy.html
    https://ffideo.gesuvik.lol/eula.html
    https://ffideo.gesuvik.lol/refunds.html
    https://ffideo.gesuvik.lol/success.html
    ```

GitHub may display a different Pages target for an organization repository. If so, use the exact target GitHub shows in **Settings → Pages** rather than guessing it.

## Content provenance

The legal/install pages are rendered from the existing FFideo release drafts. Exact copies are kept in [`release-docs/`](release-docs/):

- `PRIVACY.md`
- `EULA.md`
- `REFUNDS.md`
- `INSTALL.md`
- `UNINSTALL.md`
- `CHANGELOG.md`
- `rollback.md`

Those documents remain visibly marked provisional where the source says owner, legal, Merchant of Record, store-configuration, or publication approval is still required. Lemon Squeezy is described only as the Merchant of Record and checkout processor; the site does not claim completed legal review or unimplemented commerce automation.

The FFideo icon assets were copied from the FFideo application repository's `Resources/Branding` directory.
