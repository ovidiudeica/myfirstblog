# My First Blog

A simple personal blog created as a **GitHub Learning Lab** GitHub Pages exercise in July 2020. The site uses **Jekyll** and the **Minima** theme and is hosted on **GitHub Pages**.

**Live website:** https://ovidiudeica.github.io/myfirstblog/

## Contents

- A welcome page titled “Welcome to my blog”.
- An introductory post from 5 July 2020, also titled “Welcome to my blog”.

This repository preserves the original learning-exercise content.

## Project files

| Path | Purpose |
| --- | --- |
| `index.md` | Homepage content |
| `_posts/2020-07-05-my-first-blog-post.md` | Original blog post |
| `_config.yml` | Jekyll site settings and social-preview metadata |
| `assets/images/og-preview-sharp.png` | Image used in the site's LinkedIn/Open Graph link preview |
| `LICENSE` | MIT license and attribution |

## Making changes

Edit `index.md` to update the homepage. Jekyll blog posts are stored in `_posts/` and use the `YYYY-MM-DD-title.md` filename convention. The site is published through GitHub Pages; the Jekyll theme and the public URL are configured in `_config.yml`.


## Publishing through GitHub Actions (since 28 October 2026)

This site uses **Settings → Pages → Source: GitHub Actions**, not branch-based Pages Jekyll builds.
The `github-pages` environment permits deployments only from the protected `master`
branch; administrative bypass of environment protection was disabled during the cutover.
Deployment is **manual only**, never automatic on `push` or pull requests.

1. Open [Container-free Pages workflow](https://github.com/ovidiudeica/myfirstblog/actions/workflows/pages-migration-preview.yml).
2. Choose **Run workflow**, select `master`, enable
   **Confirm Settings > Pages > Source is GitHub Actions**, then run **once**.
3. Check that both the `preview` (Jekyll build and vulnerability audit) and
   `deploy` jobs complete successfully. Do not mistake green Dependabot PR
   previews for production deployments.
4. Check the live site, canonical and Open Graph metadata, original content and assets.
   The branch's required CI must pass before deployment. The deployment job uses
   `actions/deploy-pages`; the build uses the committed `Gemfile.lock`, not
   GitHub's managed `jekyll-build-pages` container.

**Emergency rollback:** stop manual deployment; if publication is broken, switch
**Settings → Pages → Build and deployment → Source** back to
**Deploy from a branch → master → /(root)**. This restores the old path but
**reintroduces the provider-managed Jekyll image risk**: re-open
[the tracked security issue](https://github.com/ovidiudeica/myfirstslideshow/issues/32)
and reinstate the Actions workflow once repaired. Rollback never requires
force-pushing or disabling branch protection.

## Origins and license

This repository began as a GitHub Learning Lab GitHub Pages exercise. The original text and post are retained. See [LICENSE](LICENSE) for the MIT license and original copyright notice.
