<?php
/* Smarty version 3.1.48, created on 2024-11-14 18:21:48
  from '/var/www/html/admin-dev/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_673631ac1de427_90751808',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '0193d16a77e393793d93170cae6e4dd6053d838c' => 
    array (
      0 => '/var/www/html/admin-dev/themes/default/template/content.tpl',
      1 => 1731603443,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_673631ac1de427_90751808 (Smarty_Internal_Template $_smarty_tpl) {
?><div id="ajax_confirmation" class="alert alert-success hide"></div>
<div id="ajaxBox" style="display:none"></div>

<div class="row">
	<div class="col-lg-12">
		<?php if ((isset($_smarty_tpl->tpl_vars['content']->value))) {?>
			<?php echo $_smarty_tpl->tpl_vars['content']->value;?>

		<?php }?>
	</div>
</div>
<?php }
}
