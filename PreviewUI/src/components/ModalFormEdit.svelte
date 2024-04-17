<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import { getModalStore } from '@skeletonlabs/skeleton';

	interface Risk{
		risk_title: string;
		risk_description: string;
		risk_impact? : string;
		risk_likeliness? : string;
	}

	export let parent: SvelteComponent;

	const modalStore = getModalStore();

	const formData : Risk = structuredClone($modalStore[0].meta.risk)

	function onFormSubmit(): void {
		if ($modalStore[0].response) $modalStore[0].response(formData);
		modalStore.close();
	}

	const cBase = 'card p-4 w-modal shadow-xl space-y-4';
	const cHeader = 'text-2xl font-bold';
	const cForm = 'border border-surface-500 p-4 space-y-4 rounded-container-token';
</script>


{#if $modalStore[0]}
	<div class="modal-example-form {cBase}">
		<header class={cHeader}>Edit risk</header>
		<form class="modal-form {cForm}">
			<label class="label">
				<span>Risk title</span>
				<input class="input" type="text" bind:value={formData.risk_title} placeholder="Enter title..." required/>
			</label>
			<label class="label">
				<span>Risk description</span>
                <textarea class="textarea" rows="4" bind:value={formData.risk_description} placeholder="Enter description..." required={true}/>
			</label>
			<label class="label">
				<span>Impact</span>
				<input class="input" type="text" bind:value={formData.risk_impact} placeholder="0 - 10" required/>
			</label>
			<label class="label">
				<span>Likeliness</span>
				<input class="input" type="text" bind:value={formData.risk_likeliness} placeholder="0 - 10" required/>
			</label>
		</form>
		<footer class="modal-footer {parent.regionFooter}">
			<button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
			<button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Submit</button>
		</footer>
	</div>
{/if}