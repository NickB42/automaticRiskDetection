<script lang="ts">
	import { Avatar, getModalStore, popup, getToastStore } from '@skeletonlabs/skeleton';
	import type { ModalSettings, PopupSettings, ModalComponent, ModalStore, ToastSettings } from '@skeletonlabs/skeleton';
	import csvtojson from "csvtojson";
    import { onMount } from 'svelte';
	import ModalCreateTemp from '../components/ModalFormCreate.svelte';
	import ModalForList from '../components/ModalFormEdit.svelte';


	//**--------------Interfaces--------------+*/
	interface Risk{
		risk_title: string;
		risk_description: string;
		risk_impact? : string;
		risk_likeliness? : string;
	}

	interface MessageFeed {
		id: number;
		host: boolean;
		name: string;
		timestamp: string;
		message: string;
	}

	//**--------------Constants--------------+*/
	const COMPMSG = "I am done with my analysis! I identified 5 potential risks and gave you a short description. You can now asks my anything about these risks or add them to the risk list. The risk list also allows you do analyse the risks in impact and likeliness."

	const modalStore : ModalStore = getModalStore();
	const createRiskcomp: ModalComponent = { ref: ModalCreateTemp };
	const editListcomp : ModalComponent = {ref: ModalForList}

	const modalCreateRisk: ModalSettings = {
		type: 'component',
		component: createRiskcomp,
		response(risk: any){ 
			if (risk.risk_title && risk.risk_description) riskList = [...riskList, risk]
		},
	};	

	const modalEditList: ModalSettings = {
		type: 'component',
		component: editListcomp,
		response(risk: any){ 
			if (risk) {
				let found = riskList.findIndex(r => r.risk_title == $modalStore[0].meta.risk.risk_title)
				riskList[found] = risk
			}
		},
	};	

	const popupHover: PopupSettings = {
		event: 'hover',
		target: 'popupHover',
		placement: 'bottom'
	};

	const errorToast: ToastSettings = {
		message: 'Risk export failed! Evaluate risk impact and risk likeliness first.',
		background: 'variant-filled-error',
	};
	const toastStore = getToastStore();


	//**--------------Variables--------------+*/
	let elemChat: HTMLElement;

	let currentMessage = '';

	let messageFeed: MessageFeed[] = [
		{
			id: 0,
			host: false,
			name: 'The Computer',
			timestamp: 'Today @ ' + getCurrentTimestamp(),
			message: "Hello, this is the computer! I'm your AI assistant for risk detection!\n\nI am already analysing your project data for potentially risks. Just wait a moment!",
		}
	];

	let mock : Risk[]= [{risk_title: "titel1", risk_description :"titel".repeat(15)},{risk_title: "titel2", risk_description :"titel\n".repeat(10)},{risk_title: "titel3", risk_description :"titel\n".repeat(15)},{risk_title: "titel4 \n".repeat(7), risk_description :"titel\n".repeat(5)},{risk_title: "titel5", risk_description :"titel\n".repeat(40)}]
	let popupRisk : Risk = {risk_title: "", risk_description :""}; 

	let risks : Risk[] = []
	let riskList : Risk[] = [];


	//**--------------Functions--------------+*/
	onMount(async()=>{
		risks = await findRisks("The list of risks is empty.")

		addMessageComp(COMPMSG)
	})

	function addToRiskList(r: any): any{
		if (r.risk_title && r.risk_description){
			if (!r.risk_impact) r.risk_impact = ""
			if (!r.risk_likeliness) r.risk_likeliness = ""
			riskList = [...riskList, r]
		}
	}

	async function findNewRisks() {
		risks = []
		addMessageComp("Working on finding new risks.")
		
		let input = "This is the list of risks from the project manager:\nrisk_title,risk_description\n"

		if(riskList.length != 0){
			riskList.forEach(r => {
			input += "\n" + r.risk_title + "," + r.risk_description
			})
		}else{
			input = "The list of risks from the project manager is empty."
		}

		risks = await findRisks(input)

		addMessageComp("I identified more risks for you.")
	}
	//**-------------Requests-----------------**//	
	async function findRisks(input:string) {
		console.log(input)
		let res = await fetch('http://localhost:3000/api/RiskPrompt/findRisks', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain',
				'user' : 'user1'
			},
			body: input
      	});
    	let ans  =  await csvtojson().fromString(await res.text())

		return await repeatRequest(ans)
	}

	async function sendChat(input:string){
		let res = await fetch('http://localhost:3000/api/RiskPrompt/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain',
				'user' : 'user1'
			},
			body: input
      	});
		return await res.text()
	}

	async function evaluateRisks() : Promise<any>{
		let input ="risk_title,risk_description"
		riskList.forEach((risk) =>{
			input += "\n" + risk.risk_title + "," + risk.risk_description
		})

		let res = await fetch('http://localhost:3000/api/RiskPrompt/evaluateRisks', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain',
				'user' : 'user1'
			},
			body: input
		});

		let ans = await csvtojson().fromString(await res.text())
		riskList = await repeatRequest(ans)

		//@ts-ignore
		riskList = riskList.toSorted((a,b) => {return ((b.risk_likeliness + b.risk_impact) - (a.risk_likeliness + a.risk_impact))})
	}

	async function exportRisks() {
		if(!riskList.every(r =>{
			return (r.risk_likeliness != "") && (r.risk_impact != "")
			})
		){
			toastStore.trigger(errorToast)
			return
		}

		let input ="risk_title,risk_description,risk_impact,risk_likeliness"
		riskList.forEach((risk) =>{
			input += "\n" + risk.risk_title + "," + risk.risk_description + "," + risk.risk_impact + "," + risk.risk_likeliness
		})

		let res = await fetch('http://localhost:3000/api/RiskPrompt/exportRisks', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain',
				'user' : 'user1'
			},
			body: input
		});

		//put it like in a popup, or keep like this idk
		console.log(await csvtojson().fromString(await res.text()))
    }

	async function repeatRequest(res: any[]){
		let iscorrectReq = res.every(r => {
			let keys = Object.keys(r)
			return keys.includes("risk_title") && keys.includes("risk_description")
		})
		if (iscorrectReq && res.length != 0) {
			return res
		}
		
		let response = await fetch('http://localhost:3000/api/RiskPrompt/tryAgain', {
			method: 'GET',
			headers: {
				'Content-Type': 'text/plain',
				'user' : 'user1'
			}
      	});

		return repeatRequest(await csvtojson().fromString(await response.text()))
	}

	async function resetHistory(){
		risks = []
		resetLocalHistory()

		await fetch('http://localhost:3000/api/RiskPrompt/deleteHistory', {
			method: 'GET',
			headers: {
				'Content-Type': 'text/plain',
				'user' : 'user1'
			}
      	});

		risks = await findRisks("The list of risks is empty.")
	}

	//**-------------MSG-----------------**//	
	function addMessage(): void {
		const newMessage = {
			id: messageFeed.length,
			host: true,
			name: 'The project manager',
			timestamp: `Today @ ${getCurrentTimestamp()}`,
			message: currentMessage,
		};
		messageFeed = [...messageFeed, newMessage];

		let response = sendChat(currentMessage)

		currentMessage = '';

		addMessageCompProm(response)

		setTimeout(() => {
			scrollChatBottom('smooth');
		}, 0);		
	}

	async function addMessageCompProm(res: any) {		
		addMessageComp(await res)
	}

	function addMessageComp(res: string) {		
		const newMessage = {
			id: messageFeed.length,
			host: false,
			name: 'The Computer',
			timestamp: `Today @ ${getCurrentTimestamp()}`,
			message: res,
		};
		messageFeed = [...messageFeed, newMessage];

		setTimeout(() => {
			scrollChatBottom('smooth');
		}, 0);	
	}


	//**-------------Util-----------------**//	
	function resetLocalHistory(){
		messageFeed = [
			{
				id: 0,
				host: false,
				name: 'The Computer',
				timestamp: 'Today @ ' + getCurrentTimestamp(),
				message: "Hello, this is the computer! I'm your AI assistant for risk detection!\n\nI am already analysing your project data for potentially risks. Just wait a moment!",
			}
		];
	}

	function scrollChatBottom(behavior?: ScrollBehavior): void {
		elemChat.scrollTo({ top: elemChat.scrollHeight, behavior });
	}

	function getCurrentTimestamp(): string {
		return new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
	}

	function onPromptKeydown(event: KeyboardEvent): void {
		if (['Enter'].includes(event.code)) {
			event.preventDefault();
			addMessage();
		}
	}
</script>
<head:svelte>
	<title>Risk Mgm PoC</title>
</head:svelte>

<section>
	<div class="grid grid-cols-4 gap-x-4 gap-y-16 my-10 mx-10">
			<!--Chat-->
			<section class="card col-span-3">
					<div class="grid grid-row-[1fr_auto]">
						<!-- Conversation -->
						<section bind:this={elemChat} class="h-[600px] m p-4 overflow-y-auto space-y-4">
							{#each messageFeed as bubble}
								{#if bubble.host === false}
									<div class="grid grid-cols-[auto_1fr] gap-2">
										<Avatar src="https://upload.wikimedia.org/wikipedia/commons/5/56/Computer_icon.png" width="w-12" />
										<div class="card p-4 variant-soft rounded-tl-none space-y-2}">
											<header class="flex justify-between items-center">
												<p class="font-bold">{bubble.name}</p>
												<small class="opacity-50">{bubble.timestamp}</small>
											</header>
											<p>{bubble.message}</p>
										</div>
									</div>
								{:else}
									<div class="grid grid-cols-[1fr_auto] gap-2">
										<div class="card p-4 rounded-tr-none space-y-2 variant-soft-primary">
											<header class="flex justify-between items-center">
												<p class="font-bold">{bubble.name}</p>
												<small class="opacity-50">{bubble.timestamp}</small>
											</header>
											<p>{bubble.message}</p>
										</div>
										<Avatar src="https://i.pravatar.cc/?img=48" width="w-12" />
									</div>
								{/if}
							{/each}
						</section>
						<!-- Prompt -->
						{#if typeof risks == "object"}
						<section class="border-t border-surface-500/30 p-4">
							<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] rounded-container-token">
								<button class="input-group-shim" on:click={resetHistory}>
									<div class="flex flex-col">
										<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6">
											<path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
										  </svg>				
										<p class="text-xs">reset</p>
									</div>					  
								</button>
								<textarea
									bind:value={currentMessage}
									class="bg-transparent border-0 ring-0"
									name="prompt"
									id="prompt"
									placeholder="Write a message..."
									on:keydown={onPromptKeydown}
								/>
								<button class="{currentMessage ? 'variant-filled-primary' : 'input-group-shim'}" on:click={addMessage}>
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
									  </svg>									  
								</button>
							</div>
						</section>
						{/if}
					</div>
			</section>
		<!--Risks-->
		<section class="card flex flex-col gap-y-5">
			<div class="h-[600px] flex flex-col" id="Risks">
				<h4 class="self-center pt-3">Risks</h4>
				<div class="flex flex-col gap-y-5 p-5">
					{#each risks as risk}
						<div class="card variant-soft flex justify-between p-3" use:popup={popupHover} on:mouseover={() => {popupRisk = risk}} role="presentation" on:focus={() => {}}>
							<p>{risk.risk_title}</p>
							<button on:click={addToRiskList(risk)} class="[&>*]:pointer-events-none">
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
								  </svg>
							</button>
						</div>
					{/each}
				</div>
			</div>
			<button class="btn variant-filled w-4/5 self-center" on:click={findNewRisks}>
				<div class="flex gap-x-4">
					<p>Find new risks</p>
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
					  </svg>					  
				</div>		
			</button>	
		</section>
	<!--RiskTable-->
	<div class="card col-span-4">
		<div class="table-container">
			<table class="table table-hover">
				<thead>
					<tr class="">
						<th class="w-[20%]">title</th>
						<th class="w-[40%]">description</th>
						<th class="w-[15%]">impact</th>
						<th class="w-[15%] table-cell-fit">Likeliness</th>
						<th class="w-[20%]">Edit / Delete</th>
					</tr>
				</thead>
				<tbody>
					{#each riskList as risk, i}
						<tr>
							<td>{risk.risk_title}</td>
							<td>{risk.risk_description}</td>
							<td class="table-cell-fit">{risk.risk_impact}</td>
							<td>{risk.risk_likeliness}</td>
							<td class="flex gap-x-2">
								<button type="button" class="btn-icon bg-initial" on:click={() =>{ modalEditList.meta = {risk : risk}; modalStore.trigger(modalEditList)}}>
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
									  </svg>															
								</button>
								<button type="button" class="btn-icon bg-initial" on:click={() => riskList = riskList.filter(r => r.risk_title != risk.risk_title)}>
									<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
										<path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
									  </svg>									  
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="flex justify-end items-center p-4">
				<button type="button" class="btn bg-initial" on:click={() =>{ modalStore.trigger(modalCreateRisk)}}>
					<span>Add risk</span>
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
				  	</svg>
				</button>
				<button type="button" class="btn bg-initial" on:click={evaluateRisks}>
					<span>Evaluate risk impact and likeliness</span>
					  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0 1 18 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3 1.5 1.5 3-3.75" />
					  </svg>													
				</button>
				<button type="button" class="btn bg-initial" on:click={exportRisks}>
					<span>Export risks</span>
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
						<path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
					  </svg>																		  
				</button>
			</div>
		</div>
	</div>
  </div>
</section>


<div class="card p-4 w-[300px]" data-popup="popupHover">
	<p>{popupRisk.risk_description}</p>
</div>