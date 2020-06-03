// Dependencies
var clone = require('git-clone');
var inquirer = require('inquirer');

// Variable for commanding the script.  I plan to be adding more functionality and this will help direct the program
var command = process.argv[2];


// Switch case for directing the script. Takes in 'command' from the 3rd parameter typed into the command line (node clone clone-repo)
switch(command) {
	case 'clone-repo':
		cloneRepo();
		break;
}


// Repo cloning function
function cloneRepo() {

	// This part leverages inquirer to obtain user input on what repository to download and (eventually) where to put it.
	inquirer.prompt([

		{
			type: "input",
			name: "githubUser",
			message: "Which user owns the repository? (Username - Case Sensitive)"
		},
		{
			type: "input",
			name: "githubRepo",
			message: "What's the repository name? (Repo Name - Case Sensitive)"
		},
		{
			type: "input",
			name: "folderName",
			message: "What would you like to name the folder the repository will be stored in?"
		},
		{
			type: "checkbox",
			name: "options",
			message: "Add custom options to repo clone? (Optional)",
			choices: ["git", "shallow", "checkout", "no thanks"]
		}

		]).then(function(user) {

			// Takes the user input and stores it in variables to be passed into the github api.
			var targetRepo = "https://github.com/" + user.githubUser + "/" + user.githubRepo;
			var targetPath = require("path").join(__dirname, user.folderName);
			var options = user.options;
			var cb = cb;

			console.log("Cloning repository into: " + targetPath);

			// Native method from the git-clone npm.  This is what does all the work.
			clone(targetRepo, targetPath, options, cb, function(err) {
				
				if (err) {
					console.log(err);
				}
				
				console.log("Cloning repository into: " + targetPath);
			});
		});
	};