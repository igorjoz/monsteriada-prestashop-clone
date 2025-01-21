{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}

<div class="block_newsletter col-lg-8 col-md-12 col-sm-12" id="blockEmailSubscription_{$hookName}">
  <div class="row">
    <p id="block-newsletter-label" class="col-md-5 col-xs-12"><span><b>Zapisz się</b> do newsletera</span></p>
    <div class="col-md-7 col-xs-12">
      <form action="{$urls.current_url}#blockEmailSubscription_{$hookName}" method="post">
        <div class="row">
          <div class="col-xs-12">
            <div class="input-wrapper">
              <input
                name="email"
                type="email"
                value="{$value}"
                align="left"
                placeholder="Wpisz swój adres e-mail"
                aria-labelledby="block-newsletter-label"
                required
              >
            </div>
            
            <div class="btn-submit-newsletter disabled" id="btn-submit-janek">
              <button
                class="btn btn-primary float-xs-right hidden-xs-down"
                name="submitNewsletter"
                type="submit"
                title="Zapisz się →"
                id="janek-submit-button"
                disabled="disabled"
              >
                Zapisz się →
              </button>
            </div>
            
            <input
              class="btn btn-primary float-xs-right hidden-sm-up"
              name="submitNewsletter"
              type="submit"
              value="{l s='OK' d='Shop.Theme.Actions'}"
            >
            
            <input type="checkbox" name="allow-newsletter" id="allow-newsletter-janek" required>
            <p>Wyrażam zgodę na otrzymywanie newslettera oraz kodów rabatowych na podany adres e-mail. Więcej informacji w <a class="janek-link" href="/content/3-polityka-prywatnosci">Polityce Prywatności</a>. *</p>
            <input type="hidden" name="blockHookName" value="{$hookName}" />
            <input type="hidden" name="action" value="0">
            <div class="clearfix"></div>
          </div>
          <div class="col-xs-12">
              {if $msg}
                <p class="alert {if $nw_error}alert-danger{else}alert-success{/if}">
                  {$msg}
                </p>
              {/if}
              {hook h='displayNewsletterRegistration'}
              {if isset($id_module)}
                {hook h='displayGDPRConsent' id_module=$id_module}
              {/if}
          </div>
        </div>
      </form>
    </div>
    <script>
      // Get the checkbox and button elements
      const checkbox = document.getElementById('allow-newsletter-janek');
      const submitButton = document.getElementById('janek-submit-button');
      const parentDiv = document.getElementById('btn-submit-janek');

      // Add an event listener to the checkbox
      checkbox.addEventListener('change', () => {
          if (checkbox.checked) {
              // Enable the submit button
              submitButton.removeAttribute('disabled');
              parentDiv.classList.remove('disabled');
          } else {
              // Disable the submit button
              submitButton.setAttribute('disabled', 'true');
              parentDiv.classList.add('disabled');
          }
      });
    </script>
  </div>
</div>
